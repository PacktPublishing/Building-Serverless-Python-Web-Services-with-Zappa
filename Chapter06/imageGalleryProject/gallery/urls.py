from django.urls import path, include
from rest_framework import routers
from gallery.views import PhotoAlbumViewset, PhotoViewset

router = routers.DefaultRouter()
router.register('albums', PhotoAlbumViewset)
router.register('albums/(?P<album_id>[0-9]+)/photos', PhotoViewset)

urlpatterns = [
    path(r'', include(router.urls)),
]
