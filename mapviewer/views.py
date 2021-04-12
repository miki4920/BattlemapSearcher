from django.http import FileResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

from .csrf import CsrfExemptSessionAuthentication
from .models import Map, MapBlacklist
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


@csrf_exempt
def request_map(request, map_id):
    if request.method == "GET":
        return get_map(map_id)
    elif request.method == "DELETE":
        return delete_map(map_id)


def get_map(map_id):
    map_file = get_object_or_404(Map, id=map_id)
    response = HttpResponse(map_file.picture.read())
    extension = "png" if map_file.extension == "png" else "jpeg"
    response['Content-Type'] = f'image/{extension}'
    response['Content-Disposition'] = f'attachment; filename={map_file.name}.{map_file.extension}'
    return response


def delete_map(map_id):
    map_file = get_object_or_404(Map, id=map_id)
    MapBlacklist.objects.create_map_black_list(map_file.hash)
    map_file.delete()
    response = HttpResponse()
    response.status_code = 204
    return response
