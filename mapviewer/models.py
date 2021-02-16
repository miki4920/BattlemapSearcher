from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50)


class MapManager(models.Manager):
    def create_map(self, name, extension, picture, uploader):
        battlemap = self.create(name=name, extension=extension, picture=picture, uploader=uploader)
        return battlemap


class Map(models.Model):
    name = models.CharField(max_length=50)
    extension = models.CharField(max_length=3)
    picture = models.ImageField(upload_to="maps")
    uploader = models.CharField(max_length=50)

    objects = MapManager()

    @classmethod
    def create(cls, name, extension, picture, uploader):
        battlemap = cls(name=name, extension=extension, picture=picture, uploader=uploader)
        return battlemap




