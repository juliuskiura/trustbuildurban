from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from .models import (
    AvailableHomesPage,
    AvailableHomesHeroSection,
    AvailableHomesCTASection,
    AvailableHome,
    AvailableHomeImage,
    BathroomInformation,
    BedroomInformation,
    HeatingAndCooling,
    KitchenAndDining,
    InteriorFeatures,
    OtherRooms,
    GarageAndParking,
    UtilitiesAndGreenEnergy,
    OutdoorSpaces,
)


@admin.register(AvailableHomesPage)
class AvailableHomesPageAdmin(admin.ModelAdmin):
    list_display = ["title", "is_published", "created_at"]
    list_filter = ["is_published"]
    search_fields = ["title"]


@admin.register(AvailableHomesHeroSection)
class AvailableHomesHeroSectionAdmin(admin.ModelAdmin):
    list_display = ["__str__", "available_homes_page", "title"]
    raw_id_fields = ["available_homes_page"]
    search_fields = ["available_homes_page__title", "title"]


@admin.register(AvailableHomesCTASection)
class AvailableHomesCTASectionAdmin(admin.ModelAdmin):
    list_display = ["__str__", "available_homes_page", "title"]
    raw_id_fields = ["available_homes_page"]
    search_fields = ["available_homes_page__title", "title"]


class AvailableHomeImageInline(admin.TabularInline):
    """Inline admin for AvailableHomeImage model."""

    model = AvailableHomeImage
    extra = 1
    can_delete = True
    fieldsets = ((None, {"fields": ("image", "image_url", "is_cover")}),)


@admin.register(AvailableHome)
class AvailableHomeAdmin(OrderedModelAdmin):
    list_display = [
        "__str__",
        "title",
        "location",
        "price",
        "status",
        "is_featured",
        "order",
    ]
    list_filter = ["status", "is_featured"]
    search_fields = ["title", "location", "price"]
    raw_id_fields = ["image"]
    inlines = [AvailableHomeImageInline]


@admin.register(BathroomInformation)
class BathroomInformationAdmin(admin.ModelAdmin):
    list_display = ["__str__", "home", "title", "value"]
    search_fields = ["home__title", "title"]
    raw_id_fields = ["home"]
    ordering = ["id"]


@admin.register(BedroomInformation)
class BedroomInformationAdmin(admin.ModelAdmin):
    list_display = ["__str__", "home", "title", "value"]
    search_fields = ["home__title", "title"]
    raw_id_fields = ["home"]
    ordering = ["id"]


@admin.register(HeatingAndCooling)
class HeatingAndCoolingAdmin(admin.ModelAdmin):
    list_display = ["__str__", "home", "title", "value"]
    search_fields = ["home__title", "title"]
    raw_id_fields = ["home"]
    ordering = ["id"]


@admin.register(KitchenAndDining)
class KitchenAndDiningAdmin(admin.ModelAdmin):
    list_display = ["__str__", "home", "title", "value"]
    search_fields = ["home__title", "title"]
    raw_id_fields = ["home"]
    ordering = ["id"]


@admin.register(InteriorFeatures)
class InteriorFeaturesAdmin(admin.ModelAdmin):
    list_display = ["__str__", "home", "title", "value"]
    search_fields = ["home__title", "title"]
    raw_id_fields = ["home"]
    ordering = ["id"]


@admin.register(OtherRooms)
class OtherRoomsAdmin(admin.ModelAdmin):
    list_display = ["__str__", "home", "title", "value"]
    search_fields = ["home__title", "title"]
    raw_id_fields = ["home"]
    ordering = ["id"]


@admin.register(GarageAndParking)
class GarageAndParkingAdmin(admin.ModelAdmin):
    list_display = ["__str__", "home", "title", "value"]
    search_fields = ["home__title", "title"]
    raw_id_fields = ["home"]
    ordering = ["id"]


@admin.register(UtilitiesAndGreenEnergy)
class UtilitiesAndGreenEnergyAdmin(admin.ModelAdmin):
    list_display = ["__str__", "home", "title", "value"]
    search_fields = ["home__title", "title"]
    raw_id_fields = ["home"]
    ordering = ["id"]


@admin.register(OutdoorSpaces)
class OutdoorSpacesAdmin(admin.ModelAdmin):
    list_display = ["__str__", "home", "title"]
    search_fields = ["home__title", "title"]
    raw_id_fields = ["home"]
    ordering = ["id"]
