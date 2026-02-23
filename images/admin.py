from django.contrib import admin
from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["alt_text", "caption", "created_at"]
    search_fields = ['alt_text', 'caption']
    ordering = ["-created_at"]
