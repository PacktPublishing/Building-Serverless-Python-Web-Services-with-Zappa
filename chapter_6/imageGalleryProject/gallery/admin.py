from django.contrib import admin
from django.utils.html import mark_safe
from gallery.models import PhotoAlbum, Photo
# Register your models here.

class PhotoAdminInline(admin.TabularInline):
    model = Photo
    extra = 1
    fields = ( 'image', 'image_tag', )
    readonly_fields = ('image_tag',)

    def image_tag(self, instance):
        if instance.image_thumbnail.name:
            return mark_safe('<img src="%s" />' % instance.image_thumbnail.url)
        return ''
    image_tag.short_description = 'Image Thumbnail'

class PhotoAlbumAdmin(admin.ModelAdmin):
    inlines = [PhotoAdminInline]


admin.site.register(PhotoAlbum, PhotoAlbumAdmin)