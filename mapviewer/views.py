from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

from .csrf import CsrfExemptSessionAuthentication
from .models import Map


class MapUpload(APIView):
    parser_classes = (MultiPartParser, FormParser, )
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request):
        name = request.data['name']
        extension = request.data['extension']
        picture = request.data['picture']
        uploader = request.data['uploader']
        map_model = Map.objects.create_map(name=name, extension=extension, picture=picture, uploader=uploader)
        map_model.save()
        return Response(status=201)

