from django.db import models
from .config import CONFIG
from .images import create_thumbnail


class TagManager(models.Manager):
    def create_tag(self, tag_name):
        tag = self.create(name=tag_name)
        return tag


class Tag(models.Model):
    name = models.CharField(max_length=50)

    objects = TagManager()

    @classmethod
    def create(cls, tag_name):
        tag = cls(name=tag_name)
        return tag

    def __str__(self):
        return self.name


class MapManager(models.Manager):
    def create_map(self, map_dictionary):
        name = map_dictionary["name"]
        extension = map_dictionary["extension"]
        picture = map_dictionary["picture"]
        thumbnail = create_thumbnail(picture)
        uploader = map_dictionary["uploader"]
        width = map_dictionary["width"]
        height = map_dictionary["height"]
        square_width = map_dictionary["square_width"]
        square_height = map_dictionary["square_height"]
        battlemap = self.create(name=name, extension=extension, picture=picture, thumbnail=thumbnail, uploader=uploader, width=width,
                                height=height, square_width=square_width, square_height=square_height)
        return battlemap


class Map(models.Model):
    name = models.CharField(max_length=CONFIG.NAME_LENGTH)
    extension = models.CharField(max_length=3)
    picture = models.ImageField(upload_to=CONFIG.UPLOAD_DIRECTORY)
    thumbnail = models.ImageField(upload_to=CONFIG.THUMBNAIL_DIRECTORY)
    uploader = models.CharField(max_length=CONFIG.NAME_LENGTH)
    width = models.IntegerField()
    height = models.IntegerField()
    square_width = models.IntegerField(null=True)
    square_height = models.IntegerField(null=True)
    tags = models.ManyToManyField(Tag)

    objects = MapManager()

    @classmethod
    def create(cls, map_dictionary):
        name = map_dictionary["name"]
        extension = map_dictionary["extension"]
        picture = map_dictionary["picture"]
        thumbnail = create_thumbnail(picture)
        uploader = map_dictionary["uploader"]
        width = map_dictionary["width"]
        height = map_dictionary["height"]
        square_width = map_dictionary["square_width"]
        square_height = map_dictionary["square_height"]

        battlemap = cls(name=name, extension=extension, picture=picture, thumbnail=thumbnail, uploader=uploader, width=width,
                        height=height, square_width=square_width, square_height=square_height)
        return battlemap
