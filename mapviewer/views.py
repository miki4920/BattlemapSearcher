from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

from .csrf import CsrfExemptSessionAuthentication
from .models import Map, Tag
from .verificators import get_map_dictionary
from .errors import *
from random import choice


class MapUpload(APIView):
    parser_classes = (MultiPartParser, FormParser,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request):
        try:
            map_dictionary = get_map_dictionary(request.data)
        except VerificationError as e:
            response = Response(status=400)
            response.content = str(e)
            return response

        map_model = Map.objects.create_map(map_dictionary=map_dictionary)
        map_model.save()
        for tag in map_dictionary["tags"]:
            if Tag.objects.filter(name=tag).count() == 0:
                tag = Tag.objects.create_tag(tag_name=tag)
                tag.save()
                map_model.tags.add(tag)
            else:
                tag = Tag.objects.filter(name=tag)[0]
                map_model.tags.add(tag)
        return Response(status=201)


def index(request):
    maps = list(Map.objects.all())
    maps = [choice(maps) for _ in range(0, 50)]
    context = {"maps": maps}
    return render(request, 'mapviewer/mapviewer.html', context)
