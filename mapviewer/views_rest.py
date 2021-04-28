import re
import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

from .errors import VerificationError
from .models import Map, MapBlacklist, Tag


@csrf_exempt
def request_map(request, map_id=None):
    if request.method == "GET":
        if map_id:
            return get_map(request, map_id)
        return get_maps()
    elif request.method == "POST":
        return post_map(request)
    elif request.method == "PUT":
        return put_map(request, map_id)
    elif request.method == "DELETE":
        return delete_map(map_id)


def get_maps():
    map_ids = []
    map_query = list(Map.objects.all().values("id"))
    for dictionary in map_query:
        map_ids.append(str(dictionary.get("id")))
    if len(map_ids) == 0:
        response = HttpResponse(status=404, content="Maps not in the database.")
        return response
    map_ids = ",".join(map_ids)
    response = HttpResponse(status=200, content=map_ids, content_type="text/plain")
    return response


def get_map_or_404(map_id):
    try:
        map_model = Map.objects.get(id=map_id)
    except Map.DoesNotExist:
        response = HttpResponse(status=404, content=f"Map {map_id} not in the database")
        return response
    return map_model


def get_map(request, map_id):
    map_model = get_map_or_404(map_id)
    if isinstance(map_model, HttpResponse):
        return map_model
    map_model = model_to_dict(map_model)
    map_model["picture"] = request.get_host() + map_model["picture"].url
    map_model["thumbnail"] = request.get_host() + map_model["thumbnail"].url
    map_model["tags"] = [str(tag) for tag in map_model["tags"]]
    map_model = json.dumps(map_model)
    response = HttpResponse(status=200, content=map_model, content_type="application/json")
    return response


def get_image(map_id):
    map_model = get_map_or_404(map_id)
    if isinstance(map_model, HttpResponse):
        return map_model
    response = HttpResponse(map_model.picture.read(), status=200)
    extension = "png" if map_model.extension == "png" else "jpeg"
    response['Content-Type'] = f'image/{extension}'
    response['Content-Disposition'] = f'attachment; filename={map_model.name}.{map_model.extension}'
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