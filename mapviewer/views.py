import random
import re
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Map, MapBlacklist, Tag
from .errors import VerificationError
from .forms import SearchForm
from .config import CONFIG
from .utility import get_map_query


def get_seed(request):
    if request.COOKIES.get('seed'):
        seed = request.COOKIES.get('seed')
    else:
        seed = random.randint(1, 1000)
    random.seed(seed)
    return seed


def map_tiles(request):
    maps = []
    count = 0
    form = SearchForm()
    page = 1
    seed = get_seed(request)
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            page = form.cleaned_data["page"]
            maps = get_map_query(text)
            count = len(maps)
            maps = maps[0+(CONFIG.MAPS_PER_PAGE*(page-1)):CONFIG.MAPS_PER_PAGE*page]
            random.shuffle(maps)
    elif request.method == 'GET':
        maps = list(Map.objects.all())
        count = len(maps)
        maps = maps[0:CONFIG.MAPS_PER_PAGE]
        random.shuffle(maps)
    back = False if page == 1 else True
    forward = True if CONFIG.MAPS_PER_PAGE*page < count else False
    context = {"maps": maps, "search_form": form, "back": back, "forward": forward}
    request_render = render(request, 'mapviewer/map_tiles.html', context)
    request_render.set_cookie("seed", seed)
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
        return delete_map(map_id)


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
