from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import (
    HomePage,
    HeroSection,
    Stats,
    StatsSection,
    ClientReview,
    # New models
    DiasporaSection,
    DiasporaChallenge,
    FeaturesSection,
    Feature,
    StepsSection,
    Step,
    ServicesSection,
    Service,
    NewsletterSection,
)
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


class ClientReviewInline(admin.StackedInline):
    """
    Inline admin for ClientReview model.
    """

    model = ClientReview
    extra = 1
    can_delete = True
    fieldsets = (
        (None, {"fields": ("rating", "total_reviews", "label_text")}),
        (
            "Button",
            {"fields": ("button_text", "button_link")},
        ),
    )


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


class StatsSectionInline(admin.StackedInline):
    """
    Inline admin for StatsSection model.
    """

    model = StatsSection
    extra = 1
    can_delete = True
    inlines = [ClientReviewInline]
    fieldsets = (
        (
            "Quote",
            {"fields": ("quote_text",)},
        ),
        (
            "Landmark Projects",
            {
                "fields": ("landmark_projects_value", "landmark_projects_label_text"),
            },
        ),
    )


# ============== Diaspora Section Inlines ==============


class DiasporaChallengeInline(admin.StackedInline):
    """
    Inline admin for DiasporaChallenge model.
    """

    model = DiasporaChallenge
    extra = 1
    can_delete = True
    fieldsets = ((None, {"fields": ("title", "description", "order")}),)


class DiasporaSectionInline(admin.StackedInline):
    """
    Inline admin for DiasporaSection model.
    """

    model = DiasporaSection
    extra = 1
    can_delete = True
    inlines = [DiasporaChallengeInline]
    fieldsets = (
        (
            "Content",
            {"fields": ("eyebrow", "heading", "attribution")},
        ),
        (
            "Featured Project",
            {
                "fields": (
                    "featured_label",
                    "featured_title",
                    "featured_image",
                    "featured_image_url",
                )
            },
        ),
    )


# ============== Features Section Inlines ==============


class FeatureInline(admin.StackedInline):
    """
    Inline admin for Feature model.
    """

    model = Feature
    extra = 1
    can_delete = True
    fieldsets = ((None, {"fields": ("title", "description", "icon_path", "order")}),)


class FeaturesSectionInline(admin.StackedInline):
    """
    Inline admin for FeaturesSection model.
    """

    model = FeaturesSection
    extra = 1
    can_delete = True
    inlines = [FeatureInline]
    fieldsets = (
        (
            "Content",
            {"fields": ("eyebrow", "heading")},
        ),
    )


# ============== Steps Section Inlines ==============


class StepInline(admin.StackedInline):
    """
    Inline admin for Step model.
    """

    model = Step
    extra = 1
    can_delete = True
    fieldsets = ((None, {"fields": ("title", "description", "order")}),)


class StepsSectionInline(admin.StackedInline):
    """
    Inline admin for StepsSection model.
    """

    model = StepsSection
    extra = 1
    can_delete = True
    inlines = [StepInline]
    fieldsets = (
        (
            "Content",
            {"fields": ("eyebrow", "heading", "description")},
        ),
    )


# ============== Services Section Inlines ==============


class ServiceInline(admin.StackedInline):
    """
    Inline admin for Service model.
    """

    model = Service
    extra = 1
    can_delete = True
    fieldsets = (
        (None, {"fields": ("title", "description", "icon", "expertise", "order")}),
    )


class ServicesSectionInline(admin.StackedInline):
    """
    Inline admin for ServicesSection model.
    """

    model = ServicesSection
    extra = 1
    can_delete = True
    inlines = [ServiceInline]
    fieldsets = (
        (
            "Content",
            {"fields": ("subtitle", "heading")},
        ),
    )


# ============== Newsletter Section Inlines ==============


class NewsletterSectionInline(admin.StackedInline):
    """
    Inline admin for NewsletterSection model.
    """

    model = NewsletterSection
    extra = 1
    can_delete = True
    inlines = [ButtonInline]
    fieldsets = (
        (
            "Content",
            {"fields": ("heading", "description", "placeholder")},
        ),
    )


@admin.register(HomePage)
class HomePageAdmin(MPTTModelAdmin):
    """
    Admin for HomePage model.
    """
    inlines = [
        HeroSectionInline,
        StatsSectionInline,
        DiasporaSectionInline,
        FeaturesSectionInline,
        StepsSectionInline,
        ServicesSectionInline,
        NewsletterSectionInline,
    ]

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
    search_fields = ["title", "slug", "meta_title", "meta_description"]
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
                    "meta_title",
                    "meta_description",
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


@admin.register(StatsSection)
class StatsSectionAdmin(admin.ModelAdmin):
    """Admin for StatsSection model"""

    list_display = ["__str__", "homepage", "quote_text"]
    search_fields = ["homepage__title", "quote_text"]
    inlines = [ClientReviewInline]


@admin.register(ClientReview)
class ClientReviewAdmin(admin.ModelAdmin):
    """Admin for ClientReview model"""

    list_display = ["__str__", "stats_section", "rating", "total_reviews"]
    search_fields = ["stats_section__homepage__title", "total_reviews"]


# ============== Register New Models ==============


@admin.register(DiasporaSection)
class DiasporaSectionAdmin(admin.ModelAdmin):
    """Admin for DiasporaSection model"""

    list_display = ["__str__", "homepage", "eyebrow"]
    search_fields = ["homepage__title", "eyebrow", "heading"]
    inlines = [DiasporaChallengeInline]


@admin.register(DiasporaChallenge)
class DiasporaChallengeAdmin(admin.ModelAdmin):
    """Admin for DiasporaChallenge model"""

    list_display = ["__str__", "diaspora_section", "title", "order"]
    search_fields = ["diaspora_section__homepage__title", "title"]
    list_filter = ["diaspora_section"]


@admin.register(FeaturesSection)
class FeaturesSectionAdmin(admin.ModelAdmin):
    """Admin for FeaturesSection model"""

    list_display = ["__str__", "homepage", "eyebrow"]
    search_fields = ["homepage__title", "eyebrow", "heading"]
    inlines = [FeatureInline]


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    """Admin for Feature model"""

    list_display = ["__str__", "features_section", "title", "order"]
    search_fields = ["features_section__homepage__title", "title"]
    list_filter = ["features_section"]


@admin.register(StepsSection)
class StepsSectionAdmin(admin.ModelAdmin):
    """Admin for StepsSection model"""

    list_display = ["__str__", "homepage", "eyebrow"]
    search_fields = ["homepage__title", "eyebrow", "heading"]
    inlines = [StepInline]


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    """Admin for Step model"""

    list_display = ["__str__", "steps_section", "title", "order"]
    search_fields = ["steps_section__homepage__title", "title"]
    list_filter = ["steps_section"]


@admin.register(ServicesSection)
class ServicesSectionAdmin(admin.ModelAdmin):
    """Admin for ServicesSection model"""

    list_display = ["__str__", "homepage", "subtitle"]
    search_fields = ["homepage__title", "subtitle", "heading"]
    inlines = [ServiceInline]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Admin for Service model"""

    list_display = ["__str__", "services_section", "title", "order"]
    search_fields = ["services_section__homepage__title", "title"]
    list_filter = ["services_section"]


@admin.register(NewsletterSection)
class NewsletterSectionAdmin(admin.ModelAdmin):
    """Admin for NewsletterSection model"""

    list_display = ["__str__", "homepage", "heading"]
    search_fields = ["homepage__title", "heading", "cta_text"]
