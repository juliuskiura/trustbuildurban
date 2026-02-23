from django.contrib import admin
from .models import Image, ImageUsage


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["alt_text", "caption", "usage_count", "created_at"]
    search_fields = ['alt_text', 'caption']
    ordering = ["-created_at"]

    def get_readonly_fields(self, request, obj=None):
        # Add usage_count and used_by_models as readonly
        readonly = list(super().get_readonly_fields(request, obj) or [])
        readonly.extend(["usage_count", "used_by_models"])
        return readonly


@admin.register(ImageUsage)
class ImageUsageAdmin(admin.ModelAdmin):
    list_display = ["image", "content_type", "object_id", "created_at"]
    list_filter = ["content_type"]
    search_fields = ["image__alt_text", "image__caption"]
    ordering = ["-created_at"]
    raw_id_fields = ["image"]
