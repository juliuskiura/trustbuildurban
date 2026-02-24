from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from .models import (
    PortfolioPage,
    PortfolioHeader,
    PortfolioProjectsSection,
    PortfolioProjectCategory,
    PortfolioProject,
    ProjectImage,
)


@admin.register(PortfolioPage)
class PortfolioPageAdmin(admin.ModelAdmin):
    list_display = ["title", "is_published", "created_at"]
    list_filter = ["is_published"]
    search_fields = ["title"]


@admin.register(PortfolioHeader)
class PortfolioHeaderAdmin(admin.ModelAdmin):
    list_display = ["__str__", "portfolio_page", "heading"]
    raw_id_fields = ["portfolio_page"]
    search_fields = ["portfolio_page__title", "heading"]


@admin.register(PortfolioProjectsSection)
class PortfolioProjectsSectionAdmin(admin.ModelAdmin):
    list_display = ["__str__", "portfolio_page", "learn_more_text"]
    raw_id_fields = ["portfolio_page"]
    search_fields = ["portfolio_page__title"]


@admin.register(PortfolioProjectCategory)
class PortfolioProjectCategoryAdmin(OrderedModelAdmin):
    list_display = ["__str__", "name", "order"]
    search_fields = ["name"]


class ProjectImageInline(admin.TabularInline):
    """Inline admin for ProjectImage model."""

    model = ProjectImage
    extra = 1
    can_delete = True
    fieldsets = ((None, {"fields": ("image", "image_url", "is_cover")}),)


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(OrderedModelAdmin):
    list_display = [
        "__str__",
        "category",
        "title",
        "status",
        "duration",
        "highlight_project",
        "order",
    ]
    list_filter = ["category", "status", "highlight_project"]
    search_fields = ["title", "location"]
    inlines = [ProjectImageInline]
