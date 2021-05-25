import random

from django.http import HttpResponse
from django.shortcuts import render

from .config import CONFIG
from .models import Map
from .utility import clean_search, get_map_query, get_map_or_404


def get_seed(request):
    if request.COOKIES.get('seed'):
        seed = request.COOKIES.get('seed')
    else:
        seed = random.randint(1, 1000)
    random.seed(seed)
    return seed


def map_tiles(request):
    maps = []
    seed = get_seed(request)
    page = None
    count = 0
    if request.method == 'GET':
        if request.GET.get("search"):
            maps = get_map_query(clean_search(request.GET.get("search")))
        else:
            maps = Map.objects.all()
        count = maps.count()
        page = request.GET.get("page")
    page = int(page) if page else 1
    maps = list(maps)[CONFIG.MAPS_PER_PAGE*(page-1):CONFIG.MAPS_PER_PAGE*page]
    random.shuffle(maps)
    back = False if page == 1 else True
    forward = True if CONFIG.MAPS_PER_PAGE*page < count else False
    context = {"maps": maps, "back": back, "forward": forward}
    request_render = render(request, 'mapviewer/map_tiles.html', context)
    request_render.set_cookie("seed", seed)
    return request_render


def get_picture(request, map_id):
    map_model = get_map_or_404(map_id)
    if isinstance(map_model, HttpResponse):
        return map_model
    response = HttpResponse(map_model.picture.read(), status=200)
    extension = "png" if map_model.extension == "png" else "jpeg"
    response['Content-Type'] = f'image/{extension}'
    response['Content-Disposition'] = f'attachment; filename={map_model.name}.{map_model.extension}'
    return response


# TODO: add a code for fetching image link
