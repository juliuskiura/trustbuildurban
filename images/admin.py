from django.contrib import admin
from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['alt_text', 'caption', 'is_featured', 'order', 'created_at']
    list_filter = ['is_featured', 'content_type']
    search_fields = ['alt_text', 'caption']
    ordering = ['order', '-created_at']
