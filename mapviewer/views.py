from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Map, MapBlacklist
from .errors import VerificationError
from .forms import SearchForm
from random import shuffle


def map_tiles(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            tag = form.cleaned_data["text"]
            maps = list(Map.objects.filter(tags__name=tag))
    else:
        maps = list(Map.objects.all())
        shuffle(maps)
        form = SearchForm()
    context = {"maps": maps, "form": form}
    return render(request, 'mapviewer/map_tiles.html', context)


@csrf_exempt
def request_map(request, map_id=None):
    if request.method == "GET":
        return get_map(map_id)
    elif request.method == "POST":
        return post_map(request)
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


def delete_map(map_id):
    map_file = get_object_or_404(Map, id=map_id)
    MapBlacklist.objects.create_map_black_list(map_file.hash)
    map_file.delete()
    response = HttpResponse()
    response.status_code = 204
    return response
