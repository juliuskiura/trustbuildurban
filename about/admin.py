from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from .models import AboutPage, HeroSection, Stat, CorePillarsSection, Pillar


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ["title", "is_published", "created_at"]
    list_filter = ["is_published"]
    search_fields = ["title"]


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ["about_page", "eyebrow", "heading"]
    raw_id_fields = ["about_page", "image"]
    search_fields = ["about_page__title", "eyebrow", "heading"]


@admin.register(Stat)
class StatAdmin(OrderedModelAdmin):
    list_display = ["__str__", "hero_section", "order"]
    list_filter = ["hero_section"]
    raw_id_fields = ["hero_section"]


@admin.register(CorePillarsSection)
class CorePillarsSectionAdmin(admin.ModelAdmin):
    list_display = ["about_page", "eyebrow", "heading"]
    raw_id_fields = ["about_page"]
    search_fields = ["about_page__title", "eyebrow", "heading"]


@admin.register(Pillar)
class PillarAdmin(OrderedModelAdmin):
    list_display = ["__str__", "core_pillars_section", "order"]
    list_filter = ["core_pillars_section"]
    raw_id_fields = ["core_pillars_section"]
