from django.db import models
from django.utils.translation import gettext as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


# Create your models here.


def upload_path(instance, filename):
    return '{}/{}'.format(instance.album.name, filename)


class PhotoAlbum(models.Model):
    name = models.CharField(_('album name'), max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'photo_album'
        verbose_name = 'photo album'
        verbose_name_plural = 'photo albums'

    def __str__(self):
        return self.name

class Photo(models.Model):
    album = models.ForeignKey(PhotoAlbum, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(_('image'), upload_to=upload_path)
    image_thumbnail = ImageSpecField(source='image',
                                      processors=[ResizeToFill(100, 50)],
                                      format='JPEG',
                                      options={'quality': 60})
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'photo'
        verbose_name = 'photo'
        verbose_name_plural = 'photos'

    def __str__(self):
        return self.image.name.split('/')[1]
