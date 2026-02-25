from django.contrib import admin
from django.contrib.admin.actions import delete_selected
from django.utils.html import format_html
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.urls import path, reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Image, ImageUsage


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = [
        "thumbnail",
        "alt_text",
        "caption",
        "usage_count_display",
        "usage_details_display",
        "created_at",
    ]
    search_fields = ['alt_text', 'caption']
    ordering = ["-created_at"]
    readonly_fields = [
        "width",
        "height",
        "usage_count_display",
        "used_by_models_display",
        "thumbnail",
        "usage_details_display",
    ]
    fieldsets = (
        (None, {"fields": ("image", "url")}),
        ("Image Details", {"fields": ("alt_text", "caption")}),
        (
            "Metadata",
            {
                "fields": (
                    "width",
                    "height",
                    "usage_count_display",
                    "used_by_models_display",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    # Enable multiple file upload
    change_form_template = "admin/images/image/change_form.html"
    change_list_template = "admin/images/image/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "upload-multiple/",
                self.admin_site.admin_view(self.upload_multiple_view),
                name="images_image_upload_multiple",
            ),
        ]
        return custom_urls + urls

    def thumbnail(self, obj):
        """Display thumbnail of the image."""
        if obj.image_url:
            return format_html(
                '<img src="{}" style="width: 100px; height: auto; border-radius: 4px;">',
                obj.image_url,
            )
        return "-"

    thumbnail.short_description = "Preview"

    def usage_count_display(self, obj):
        """Display method for usage_count property."""
        count = obj.usage_count
        return format_html(
            '<span class="{}">{}</span>',
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

    def usage_details_display(self, obj):
        """Display detailed usage with parent hierarchy."""
        usage_info = obj.get_full_usage_info()
        if not usage_info:
            return "-"

        details = []
        for info in usage_info[:5]:
            if info.get("parent"):
                details.append(f"{info['content_type']} → {info['parent']}")
            else:
                details.append(info["content_type"])

        result = "<br>".join(details)
        if len(usage_info) > 5:
            result += f"<br>...and {len(usage_info) - 5} more"
        return format_html(result)

    usage_details_display.short_description = "Usage Details"
    usage_details_display.allow_tags = True

    @csrf_exempt
    def upload_multiple_view(self, request):
        """Handle multiple image upload."""
        from django.urls import path

        if request.method == "POST":
            files = request.FILES.getlist("images")
            uploaded_count = 0
            for f in files:
                Image.objects.create(
                    image=f,
                    alt_text=f.name.rsplit(".", 1)[0]
                    .replace("_", " ")
                    .replace("-", " ")
                    .title(),
                )
                uploaded_count += 1
            self.message_user(
                request, f"Successfully uploaded {uploaded_count} images."
            )
            return HttpResponseRedirect("../")

        # Render the upload form
        context = {
            "title": "Upload Multiple Images",
            "app_label": "images",
            "opts": self.model._meta,
        }
        return HttpResponse(
            render_to_string("admin/images/image/upload_multiple.html", context)
        )

    # Add custom actions
    actions = ["delete_selected", "upload_multiple"]

    def upload_multiple(self, request, queryset):
        """Custom action to redirect to multiple upload page."""
        return HttpResponseRedirect("upload-multiple/")

    upload_multiple.short_description = "Upload multiple images"


@admin.register(ImageUsage)
class ImageUsageAdmin(admin.ModelAdmin):
    list_display = ["image", "content_type", "object_id", "created_at"]
    list_filter = ["content_type"]
    search_fields = ["image__alt_text", "image__caption"]
    ordering = ["-created_at"]
    raw_id_fields = ["image"]
