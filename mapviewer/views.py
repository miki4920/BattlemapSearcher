import re
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Map, MapBlacklist, Tag
from .errors import VerificationError
from .forms import SearchForm
from random import randint
from .config import CONFIG


def map_tiles(request, page_id=1):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            lookup = None
            for word in text:
                if lookup:
                    lookup = lookup & (Q(tags__name__icontains=word) | Q(name__icontains=word) | Q(uploader__icontains=word))
                else:
                    lookup = (Q(tags__name__icontains=word) | Q(name__icontains=word) | Q(uploader__icontains=word))
            maps = list(Map.objects.filter(lookup).distinct())
    elif request.method == 'GET':
        if not request.GET.get("page"):
            page_id = 1
        else:
            page_id = int(request.GET.get("page")[0])
        if request.session.get('seed'):
            seed = request.session.get('seed')
        else:
            seed = randint(1, 1000)
            request.session['seed'] = seed
        request.session.set_expiry(0)
        maps = list(Map.objects.raw("SELECT * FROM mapviewer_map ORDER BY RAND(%s)" % seed))[0+(CONFIG.MAPS_PER_PAGE*(page_id-1)):CONFIG.MAPS_PER_PAGE*page_id]
        form = SearchForm()
    context = {"maps": maps, "search_form": form}
    return render(request, 'mapviewer/map_tiles.html', context)


@csrf_exempt
def request_map(request, map_id=None):
    if request.method == "GET":
        return get_map(map_id)
    elif request.method == "POST":
        return post_map(request)
    elif request.method == "PUT":
        return put_map(request, map_id)
    elif request.method == "DELETE":
        return delete_map(request)


def get_map(map_id):
    map_file = get_object_or_404(Map, id=map_id)
    response = HttpResponse(map_file.picture.read(), status=200)
    extension = "png" if map_file.extension == "png" else "jpeg"
    response['Content-Type'] = f'image/{extension}'
    response['Content-Disposition'] = f'attachment; filename={map_file.name}.{map_file.extension}'
    return response


def post_map(request):
    try:
        data = {**request.POST, **request.FILES}
        for key in data.keys():
            data[key] = data[key][0]
        Map.objects.create_map(data=data)
    except VerificationError as e:
        response = HttpResponse(status=400, content=str(e), content_type="text/plain")
        return response
    response = HttpResponse(status=201)
    return response


def put_map(request, map_id):
    map_file = get_object_or_404(Map, id=map_id)
    data = str(request.body).lower()
    if len(data) > 0:
        data = data[1:]
        data = re.sub(r"[^a-zA-Z0-9, ]", "", data)
        data = re.sub(r" ", ",", data)
        data = re.sub(r",{2,}", ",", data)
        tags = sorted(data.split(","))
        map_file.tags.clear()
        for tag in tags:
            if Tag.objects.filter(name=tag).count() == 0:
                tag = Tag.objects.create_tag(tag_name=tag)
                tag.save()
                map_file.tags.add(tag)
            else:
                tag = Tag.objects.filter(name=tag)[0]
                map_file.tags.add(tag)
        map_file.save()
        tags = [tag.capitalize() for tag in tags]
        response = HttpResponse(status=200, content=", ".join(tags)+",")
    else:
        response = HttpResponse(status=400, content="Tags cannot be empty", content_type="text/plain")
    return response


def delete_map(map_id):
    map_file = get_object_or_404(Map, id=map_id)
    MapBlacklist.objects.create_map_black_list(map_file.hash)
    map_file.delete()
    response = HttpResponse()
    response.status_code = 204
    return response
