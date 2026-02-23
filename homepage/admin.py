from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import HomePage, HeroSection, Stats
from pages.models import Button


class ButtonInline(admin.StackedInline):
    """
    Inline admin for generic Button model.
    Allows adding unlimited buttons to any component.
    """

    model = Button
    extra = 1
    can_delete = True
    fieldsets = (
        (None, {"fields": ("text", "link", "icon")}),
        (
            "Styling",
            {"fields": ("style", "size", "is_external", "is_full_width", "order")},
        ),
    )


class StatsInline(admin.StackedInline):
    """
    Inline admin for Stats model.
    """

    model = Stats
    extra = 1
    can_delete = True
    fieldsets = ((None, {"fields": ("value", "label", "icon", "order")}),)


class HeroSectionInline(admin.StackedInline):
    """
    Inline admin for HeroSection model.
    """

    model = HeroSection
    extra = 1
    max_num = 1
    can_delete = True
    inlines = [ButtonInline, StatsInline]
    fieldsets = (
        (
            "Hero Content",
            {
                "fields": (
                    "tagline",
                    "heading_main",
                    "heading_highlight",
                    "heading_suffix",
                    "description",
                )
            },
        ),
        (
            "Background Media",
            {
                "fields": (
                    "background_image",
                    "overlay_opacity",
                )
            },
        ),
        (
            "Badges & Info",
            {
                "fields": (
                    "show_verified_badge",
                    "verified_text",
                    "show_live_tracking",
                    "live_tracking_text",
                    "company_name",
                    "company_location",
                )
            },
        ),
    )


@admin.register(HomePage)
class HomePageAdmin(MPTTModelAdmin):
    """
    Admin for HomePage model.
    """
    inlines = [HeroSectionInline]

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

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    """Admin for HeroSection model"""

    list_display = ["__str__", "homepage", "tagline"]
    search_fields = ["homepage__title", "tagline"]
