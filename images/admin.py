from django.contrib import admin
from django.utils.html import format_html
from .models import Image, ImageUsage


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["alt_text", "caption", "usage_count_display", "created_at"]
    search_fields = ['alt_text', 'caption']
    ordering = ["-created_at"]
    readonly_fields = [
      
        "width",
        "height",
        "usage_count_display",
        "used_by_models_display",
    ]

    def usage_count_display(self, obj):
        """Display method for usage_count property."""
        count = obj.usage_count
        return format_html(
            '<span class="{}</span>">{}</span>',
            "text-success" if count > 0 else "text-muted",
            count,
        )

    usage_count_display.short_description = "Usage Count"
    usage_count_display.allow_tags = True

    def used_by_models_display(self, obj):
        """Display method for used_by_models property."""
        models = obj.used_by_models
        if not models:
            return "-"
        return ", ".join(models)

    used_by_models_display.short_description = "Used By"


@admin.register(ImageUsage)
class ImageUsageAdmin(admin.ModelAdmin):
    list_display = ["image", "content_type", "object_id", "created_at"]
    list_filter = ["content_type"]
    search_fields = ["image__alt_text", "image__caption"]
    ordering = ["-created_at"]
    raw_id_fields = ["image"]
