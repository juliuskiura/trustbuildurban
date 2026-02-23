from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Page, Button


@admin.register(Button)
class ButtonAdmin(admin.ModelAdmin):
    """Admin for reusable Button model"""

    list_display = ["text", "style", "size", "order", "content_type", "created_at"]
    list_filter = ["style", "size", "content_type"]
    search_fields = ["text", "link"]
    ordering = ["order", "created_at"]


@admin.register(Page)
class PageAdmin(MPTTModelAdmin):
    """
    Admin for Pages with tree structure support.
    Similar to Wagtail's page admin.
    """
    list_display = [
        'title', 
        'is_published', 
        'show_in_menus',
        'status',
        'updated_at'
    ]
    list_filter = [
        'is_published', 
        'show_in_menus',
        'created_at',
    ]
    search_fields = ['title', 'slug', 'seo_title', 'seo_description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = [
        'created_at', 
        'updated_at', 
        'revision_number',
    ]
    fieldsets = (
        (
            "Page Content",
            {
                "fields": (
                    "parent",
                    "title",
                    "slug",
                )
            },
        ),
        (
            "SEO",
            {
                "fields": (
                    "seo_title",
                    "seo_description",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Navigation",
            {
                "fields": (
                    "show_in_menus",
                    "menu_order",
                )
            },
        ),
        (
            "Publishing",
            {
                "fields": (
                    "is_published",
                    "published_date",
                    "go_live_at",
                    "expire_at",
                )
            },
        ),
        (
            "Advanced",
            {
                "fields": (
                    "custom_template",
                    "created_by",
                    "last_modified_by",
                    "revision_number",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('created_by', 'last_modified_by')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.last_modified_by = request.user
        super().save_model(request, obj, form, change)
