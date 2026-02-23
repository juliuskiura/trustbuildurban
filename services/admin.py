from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from .models import (
    ServicePage,
    ServicesHeader,
    ServicesListSection,
    Service,
)


@admin.register(ServicePage)
class ServicePageAdmin(admin.ModelAdmin):
    list_display = ["title", "is_published", "created_at"]
    list_filter = ["is_published"]
    search_fields = ["title"]


@admin.register(ServicesHeader)
class ServicesHeaderAdmin(admin.ModelAdmin):
    list_display = ["__str__", "service_page", "eyebrow", "heading"]
    raw_id_fields = ["service_page"]
    search_fields = ["service_page__title", "eyebrow", "heading"]


@admin.register(ServicesListSection)
class ServicesListSectionAdmin(admin.ModelAdmin):
    list_display = ["__str__", "service_page", "learn_more_text"]
    raw_id_fields = ["service_page"]
    search_fields = ["service_page__title"]


@admin.register(Service)
class ServiceAdmin(OrderedModelAdmin):
    list_display = ["__str__", "services_section", "title", "order"]
    list_filter = ["services_section"]
    raw_id_fields = ["services_section", "image"]
    search_fields = ["services_section__service_page__title", "title", "description"]
