from django.contrib import admin
from .models import Company, CompanyImage, ContactPerson


class CompanyImageInline(admin.TabularInline):
    model = CompanyImage
    extra = 1
    fields = ("image", "image_type", "label", "is_primary", "order")


class ContactPersonInline(admin.TabularInline):
    model = ContactPerson
    extra = 1
    fields = ("user", "first_name", "last_name", "role", "title", "email", "phone", "is_public", "order")


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "trading_name", "city", "primary_phone", "primary_email", "updated_at"]
    search_fields = ["name", "trading_name", "registration_number", "primary_email"]

    fieldsets = [
        (
            "Identity",
            {"fields": ["name", "trading_name", "tagline"]},
        ),
        (
            "Legal & Registration",
            {
                "fields": [
                    "registration_number",
                    "tax_identification_number",
                    "vat_number",
                    "year_founded",
                    "company_type",
                    "country_of_incorporation",
                ],
            },
        ),
        (
            "Physical Address",
            {
                "fields": [
                    "physical_address",
                    "city",
                    "county",
                    "country",
                    "postal_code",
                    "po_box",
                    "latitude",
                    "longitude",
                ],
                "description": (
                    "For GPS: right-click the office location in Google Maps "
                    "and copy the coordinates shown."
                ),
            },
        ),
        (
            "Contact",
            {
                "fields": [
                    "primary_phone",
                    "secondary_phone",
                    "whatsapp_number",
                    "primary_email",
                    "support_email",
                    "website",
                ],
            },
        ),
        (
            "Social Media",
            {
                "fields": [
                    "facebook_url",
                    "instagram_url",
                    "twitter_url",
                    "linkedin_url",
                    "youtube_url",
                    "tiktok_url",
                ],
                "classes": ["collapse"],
            },
        ),
    ]

    inlines = [CompanyImageInline, ContactPersonInline]


@admin.register(CompanyImage)
class CompanyImageAdmin(admin.ModelAdmin):
    list_display = ["__str__", "company", "image_type", "is_primary", "order"]
    list_filter = ["image_type", "is_primary"]
    search_fields = ["company__name", "label"]
    raw_id_fields = ["company", "image"]


@admin.register(ContactPerson)
class ContactPersonAdmin(admin.ModelAdmin):
    list_display = ["get_full_name", "company", "role", "title", "get_email", "is_public", "order"]
    list_filter = ["role", "is_public", "company"]
    search_fields = ["first_name", "last_name", "email", "user__email", "title"]
    raw_id_fields = ["company", "user", "portrait"]
    ordering = ["company", "order"]
