import random

from django.shortcuts import render

from .config import CONFIG
from .forms import SearchForm
from .models import Map
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



