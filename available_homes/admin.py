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
    ShowingRequest,
    PropertyOffer,
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
    fieldsets = ((None, {"fields": ("image", "is_cover")}),)


class BathroomInformationInline(admin.TabularInline):
    """Inline admin for BathroomInformation model."""

    model = BathroomInformation
    extra = 1
    can_delete = True
    fields = ("title", "value")


class BedroomInformationInline(admin.TabularInline):
    """Inline admin for BedroomInformation model."""

    model = BedroomInformation
    extra = 1
    can_delete = True
    fields = ("title", "value")


class HeatingAndCoolingInline(admin.TabularInline):
    """Inline admin for HeatingAndCooling model."""

    model = HeatingAndCooling
    extra = 1
    can_delete = True
    fields = ("title", "value")


class KitchenAndDiningInline(admin.TabularInline):
    """Inline admin for KitchenAndDining model."""

    model = KitchenAndDining
    extra = 1
    can_delete = True
    fields = ("title", "value")


class InteriorFeaturesInline(admin.TabularInline):
    """Inline admin for InteriorFeatures model."""

    model = InteriorFeatures
    extra = 1
    can_delete = True
    fields = ("title", "value")


class OtherRoomsInline(admin.TabularInline):
    """Inline admin for OtherRooms model."""

    model = OtherRooms
    extra = 1
    can_delete = True
    fields = ("title", "value")


class GarageAndParkingInline(admin.TabularInline):
    """Inline admin for GarageAndParking model."""

    model = GarageAndParking
    extra = 1
    can_delete = True
    fields = ("title", "value")


class UtilitiesAndGreenEnergyInline(admin.TabularInline):
    """Inline admin for UtilitiesAndGreenEnergy model."""

    model = UtilitiesAndGreenEnergy
    extra = 1
    can_delete = True
    fields = ("title", "value")


class OutdoorSpacesInline(admin.TabularInline):
    """Inline admin for OutdoorSpaces model."""

    model = OutdoorSpaces
    extra = 1
    can_delete = True
    fields = ("title", "value")


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

    inlines = [
        AvailableHomeImageInline,
        BathroomInformationInline,
        BedroomInformationInline,
        HeatingAndCoolingInline,
        KitchenAndDiningInline,
        InteriorFeaturesInline,
        OtherRoomsInline,
        GarageAndParkingInline,
        UtilitiesAndGreenEnergyInline,
        OutdoorSpacesInline,
    ]


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


@admin.register(ShowingRequest)
class ShowingRequestAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "property",
        "first_name",
        "last_name",
        "email",
        "preferred_date",
        "status",
        "created_at",
    ]
    list_filter = ["status", "preferred_time", "is_first_time_buyer", "created_at"]
    search_fields = ["property__title", "first_name", "last_name", "email", "phone"]
    raw_id_fields = ["property"]
    ordering = ["-created_at"]
    date_hierarchy = "created_at"


@admin.register(PropertyOffer)
class PropertyOfferAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "property",
        "first_name",
        "last_name",
        "offer_amount",
        "financing_type",
        "status",
        "created_at",
    ]
    list_filter = ["status", "financing_type", "is_first_time_buyer", "created_at"]
    search_fields = [
        "property__title",
        "first_name",
        "last_name",
        "email",
        "phone",
        "offer_amount",
    ]
    raw_id_fields = ["property"]
    ordering = ["-created_at"]
    date_hierarchy = "created_at"
