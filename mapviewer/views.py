from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

from .csrf import CsrfExemptSessionAuthentication
from .models import Map
from .errors import VerificationError
from .forms import SearchForm
from random import shuffle


class MapUpload(APIView):
    parser_classes = (MultiPartParser, FormParser,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @staticmethod
    def post(request):
        try:
            Map.objects.create_map(data=request.data)
        except VerificationError as e:
            response = Response(status=400)
            response.content = str(e)
            return response
        return Response(status=201)


def map_tiles(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            tag = form.cleaned_data["tag"]
            maps = list(Map.objects.filter(tags__name=tag))
    else:
        maps = list(Map.objects.all())
        shuffle(maps)
        form = SearchForm()
    context = {"maps": maps, "form": form}
    return render(request, 'mapviewer/map_tiles.html', context)


def map_tile(request, map_id):
    map_tile = get_object_or_404(Map, id=map_id)
    context = {"map": map_tile}
    return render(request, 'mapviewer/map_tile.html', context)
