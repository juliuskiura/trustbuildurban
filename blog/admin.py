from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from .models import (
    BlogPage,
    BlogHeader,
    BlogGridSection,
    BlogPost,
)


@admin.register(BlogPage)
class BlogPageAdmin(admin.ModelAdmin):
    list_display = ["title", "is_published", "created_at"]
    list_filter = ["is_published"]
    search_fields = ["title"]


@admin.register(BlogHeader)
class BlogHeaderAdmin(admin.ModelAdmin):
    list_display = ["__str__", "blog_page", "eyebrow", "heading"]
    raw_id_fields = ["blog_page"]
    search_fields = ["blog_page__title", "eyebrow", "heading"]


@admin.register(BlogGridSection)
class BlogGridSectionAdmin(admin.ModelAdmin):
    list_display = ["__str__", "blog_page", "read_more_text"]
    raw_id_fields = ["blog_page"]
    search_fields = ["blog_page__title"]


@admin.register(BlogPost)
class BlogPostAdmin(OrderedModelAdmin):
    list_display = ["__str__", "blog_section", "title", "category", "order"]
    list_filter = ["blog_section", "category"]
    raw_id_fields = ["blog_section", "image"]
    search_fields = ["blog_section__blog_page__title", "title", "category"]
