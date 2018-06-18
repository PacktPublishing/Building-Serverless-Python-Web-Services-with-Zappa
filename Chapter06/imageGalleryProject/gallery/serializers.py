from rest_framework import serializers
from gallery.models import PhotoAlbum, Photo


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ('id', 'image', 'created_at', 'updated_at')


class PhotoAlbumSerializer(serializers.ModelSerializer):

    class Meta:
        model = PhotoAlbum
        fields = ('id', 'name', 'photos', 'created_at', 'updated_at')
        depth = 1
