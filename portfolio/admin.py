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
    list_display = ["__str__", "projects_section", "name", "order"]
    list_filter = ["projects_section"]
    raw_id_fields = ["projects_section"]


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(OrderedModelAdmin):
    list_display = ["__str__", "projects_section", "title", "status", "order"]
    list_filter = ["projects_section", "status"]
    raw_id_fields = ["projects_section"]
    search_fields = ["projects_section__portfolio_page__title", "title", "location"]


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ["__str__", "project", "is_cover"]
    list_filter = ["is_cover", "project"]
    raw_id_fields = ["project", "image"]
