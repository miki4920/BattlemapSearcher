import re

from django.core.files.base import ContentFile
from django.db import models
from io import BytesIO
from PIL import Image

from .config import CONFIG
from .errors import *
from .hash import hash_picture, hash_distance
from .config import CONFIG


class TagManager(models.Manager):
    def create_tag(self, tag_name):
        tag = self.create(name=tag_name)
        return tag


class Tag(models.Model):
    name = models.CharField(max_length=CONFIG.MAXIMUM_NAME_LENGTH)
    objects = TagManager()

    @classmethod
    def create(cls, tag_name):
        tag = cls(name=tag_name)
        return tag

    def __str__(self):
        return self.name


def process_name(name):
    if re.match(r'[^a-zA-Z0-9_]', name):
        raise NameNotAlphanumerical(name)
    if not CONFIG.MINIMUM_NAME_LENGTH < len(name) < CONFIG.MAXIMUM_NAME_LENGTH:
        raise NameNotInRange(name)
    name = name.split("_")
    name = [word.capitalize() for word in name]
    name = " ".join(name)
    return name


def process_extension(extension):
    extension = extension.lower()
    if extension not in CONFIG.IMAGE_EXTENSIONS:
        raise ExtensionNotAccepted(extension)
    return extension


def process_picture(picture):
    if not CONFIG.MINIMUM_PICTURE_SIZE < len(picture) < CONFIG.MAXIMUM_PICTURE_SIZE:
        raise PictureNotInRange(picture)
    return picture


def process_hash(picture, name, ignore_hash):
    picture_hash = hash_picture(picture)
    map_hashes = Map.objects.all().values("hash")
    map_blacklist_hashes = MapBlacklist.objects.all().values("hash")
    for map_hash in map_blacklist_hashes:
        if picture_hash == map_hash["hash"]:
            raise HashNotAccepted(name)
    if not ignore_hash:
        for map_hash in map_hashes:
            if hash_distance(picture_hash, map_hash["hash"]) <= CONFIG.IMAGE_SIMILARITY:
                raise HashNotUnique(name)
    return picture_hash


def process_thumbnail(picture):
    thumbnail = Image.open(picture)
    thumbnail = thumbnail.resize((CONFIG.THUMBNAIL_SIZE, CONFIG.THUMBNAIL_SIZE), Image.ANTIALIAS)
    return thumbnail


def process_dimensions(picture):
    picture = Image.open(picture)
    width, height = picture.size
    if CONFIG.MINIMUM_IMAGE_WIDTH > width or CONFIG.MINIMUM_IMAGE_HEIGHT > height:
        raise DimensionsNotInRange(width, height)
    return width, height


def process_square_dimensions(square_width, square_height):
    if (not square_width and square_height) or (square_width and not square_height):
        raise SquareDimensionsNotAccepted(square_width, square_height)
    if (not square_width) and (not square_height):
        square_width, square_height = None, None
    if not ((square_width is None and square_height is None) or (square_width.isdigit() and square_height.isdigit())):
        raise SquareDimensionsNotInRange(square_width, square_height)
    return square_width, square_height


def process_uploader(uploader):
    if re.match(r'[^a-zA-Z_]', uploader):
        raise UploaderNotAlphanumerical(uploader)
    if not CONFIG.MINIMUM_NAME_LENGTH < len(uploader) < CONFIG.MAXIMUM_NAME_LENGTH:
        raise UploaderNotInRange(uploader)
    uploader = uploader.split("_")
    uploader = [word.capitalize() for word in uploader]
    uploader = " ".join(uploader)
    return uploader


def attach_thumbnail(name, extension, thumbnail, battlemap):
    if extension == "jpg":
        extension = "JPEG"
    else:
        extension = "PNG"
    thumbnail_io = BytesIO()
    thumbnail.save(thumbnail_io, extension, quality=60)
    battlemap.thumbnail.save(name, ContentFile(thumbnail_io.getvalue()), save=False)


def process_tags(tags):
    if tags:
        if re.match(r'^(([a-zA-Z_]{3,})([, ])?)+$', tags):
            tags = tags.split(",")
            tags = [tag.lower() for tag in tags]
        else:
            raise TagsNotAccepted(tags)
    else:
        tags = []
    return tags


class MapManager(models.Manager):
    def create_map(self, data):
        name = data.get("name")
        name = process_name(name)

        extension = data.get("extension")
        extension = process_extension(extension)

        picture = data.get("picture")
        picture = process_picture(picture)
        ignore_hash = data.get("ignore_hash")
        picture_hash = process_hash(picture, name, ignore_hash)

        thumbnail = process_thumbnail(picture)

        width, height = process_dimensions(picture)

        square_width, square_height = data.get("square_width"), data.get("square_height")
        square_width, square_height = process_square_dimensions(square_width, square_height)

        uploader = data.get("uploader")
        uploader = process_uploader(uploader)
        battlemap = self.create(name=name, extension=extension, picture=picture, hash=picture_hash,
                                width=width, height=height, square_width=square_width, square_height=square_height,
                                uploader=uploader)
        attach_thumbnail(name, extension, thumbnail, battlemap)
        tags = data.get("tags")
        tags = process_tags(tags)
        for tag in tags:
            if Tag.objects.filter(name=tag).count() == 0:
                tag = Tag.objects.create_tag(tag_name=tag)
                tag.save()
                battlemap.tags.add(tag)
            else:
                tag = Tag.objects.filter(name=tag)[0]
                battlemap.tags.add(tag)
        battlemap.save()


class Map(models.Model):
    name = models.CharField(max_length=CONFIG.MAXIMUM_NAME_LENGTH)
    extension = models.CharField(max_length=3)
    picture = models.ImageField(upload_to=CONFIG.UPLOAD_DIRECTORY)
    hash = models.CharField(max_length=16)
    thumbnail = models.ImageField(upload_to=CONFIG.THUMBNAIL_DIRECTORY)
    width = models.IntegerField()
    height = models.IntegerField()
    square_width = models.IntegerField(null=True)
    square_height = models.IntegerField(null=True)
    uploader = models.CharField(max_length=CONFIG.MAXIMUM_NAME_LENGTH)
    tags = models.ManyToManyField(Tag)
    objects = MapManager()


class MapBlacklistManager(models.Manager):
    def create_map_black_list(self, map_hash):
        map_black_list = self.create(hash=map_hash)
        map_black_list.save()


class MapBlacklist(models.Model):
    hash = models.CharField(max_length=16)
    objects = MapBlacklistManager()