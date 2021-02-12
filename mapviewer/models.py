from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50)


class Map(models.Model):
    name = models.CharField(max_length=50)
    extension = models.CharField(max_length=3)
    picture = models.ImageField(upload_to="maps")
    uploader = models.CharField(max_length=50)
    width = models.IntegerField()
    height = models.IntegerField()
    square_width = models.IntegerField()
    square_height = models.IntegerField()
    tags = models.ManyToManyField(Tag)





