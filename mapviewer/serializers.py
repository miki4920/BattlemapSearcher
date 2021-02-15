from rest_framework import serializers
from .models import Map, Tag


class MapSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    extension = serializers.CharField(max_length=3)
    picture = serializers.ImageField()
    uploader = serializers.CharField(max_length=50)
    square_width = serializers.IntegerField(required=False, allow_null=True)
    square_height = serializers.IntegerField(required=False, allow_null=True)
    tags = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=Tag.objects.all())

    def create(self, validated_data):
        return Map.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.extension = validated_data.get('extension', instance.extension)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.uploader = validated_data.get('uploader', instance.uploader)
        instance.square_width = validated_data.get('square_width', instance.square_width)
        instance.square_height = validated_data.get('square_height', instance.square_height)
        instance.tags = validated_data.get('tags', instance.tags)
        instance.save()
        return instance
