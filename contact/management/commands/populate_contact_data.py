"""
Management command to populate contact page sections data from views.py into the database models.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from contact.models import (
    ContactPage,
    ContactHeader,
    ContactContentSection,
    ContactInfo,
)


class Command(BaseCommand):
    help = "Populate contact page sections with data from views.py"

    def add_arguments(self, parser):
        parser.add_argument(
            "--contact-id",
            type=int,
            help="ID of the ContactPage to populate data for. If not provided, will use the first published ContactPage.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be created without making changes.",
        )

    def handle(self, *args, **options):
        contact_id = options.get("contact_id")
        dry_run = options.get("dry_run", False)

        # Get the ContactPage or create one if it doesn't exist
        if contact_id:
            try:
                contact_page = ContactPage.objects.get(pk=contact_id)
            except ContactPage.DoesNotExist:
                self.stderr.write(
                    self.style.ERROR(f"ContactPage with ID {contact_id} does not exist.")
                )
                return
        else:
            contact_page = ContactPage.objects.filter(is_published=True).first()
            if not contact_page:
                # Try to get any contact page
                contact_page = ContactPage.objects.first()
                if not contact_page:
                    # Create a default ContactPage
                    self.stdout.write(self.style.WARNING("No ContactPage found. Creating a default ContactPage..."))
                    contact_page = ContactPage.objects.create(
                        title="Contact",
                        slug="contact",
                        is_published=True,
                        meta_title="Contact Us | TrustBuild Urban",
                        meta_description="Get in touch with TrustBuild Urban for your premium construction and design projects in Kenya."
                    )
                    self.stdout.write(self.style.SUCCESS(f"Created ContactPage: {contact_page.title} (ID: {contact_page.pk})"))

        self.stdout.write(self.style.SUCCESS(f"Using ContactPage: {contact_page.title} (ID: {contact_page.pk})"))

        if dry_run:
            self._print_dry_run(contact_page)
            return

        # Data from views.py
        contact_header_data = {
            "eyebrow": "Get In Touch",
            "heading": "Let's Build Your Legacy Together.",
            "description": "Whether you're in the diaspora or local, we're here to provide the radical transparency and excellence your project deserves.",
        }

        contact_content_data = {
            "heading": "Contact Information",
            "items": [
                {
                    "label": "Call Us",
                    "value": "+254 712 345 678",
                    "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-phone w-5 h-5"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>""",
                },
                {
                    "label": "Email Us",
                    "value": "info@trustbuildurban.co.ke",
                    "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-mail w-5 h-5"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7"/></svg>""",
                },
                {
                    "label": "Visit Us",
                    "value": "Riverside Square, Riverside Dr,<br>Nairobi, Kenya",
                    "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-map-pin w-5 h-5"><path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/></svg>""",
                },
            ],
            "map": {
                "embed_url": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3988.808!2d36.8219!3d-1.2921!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMsKwMTdnMjAuMCJTIDM2wrA0OScxMS4wIkU!5e0!3m2!1sen!2ske!4v1234567890",
                "label": "Office Location",
            },
        }

        # Create the sections
        with transaction.atomic():
            # 1. Create or Update Contact Header
            header, created = ContactHeader.objects.update_or_create(
                contact_page=contact_page,
                defaults={
                    "eyebrow": contact_header_data["eyebrow"],
                    "heading": contact_header_data["heading"],
                    "description": contact_header_data["description"],
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} ContactHeader (ID: {header.pk})"
                )
            )

            # 2. Create or Update Contact Content Section
            content_section, created = ContactContentSection.objects.update_or_create(
                contact_page=contact_page,
                defaults={
                    "heading": contact_content_data["heading"],
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} ContactContentSection (ID: {content_section.pk})"
                )
            )

            # 3. Create Contact Info Items (with map data on first item)
            for idx, item_data in enumerate(contact_content_data["items"]):
                info, created = ContactInfo.objects.update_or_create(
                    section=content_section,
                    label=item_data["label"],
                    defaults={
                        "value": item_data["value"],
                        "icon": item_data["icon"],
                    },
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  {'Created' if created else 'Updated'} Contact Info: {info.label}"
                    )
                )

            # Add map data to the last contact info item
            if contact_content_data["items"]:
                last_item = contact_content_data["items"][-1]
                info_with_map, _ = ContactInfo.objects.update_or_create(
                    section=content_section,
                    label=last_item["label"],
                    defaults={
                        "value": last_item["value"],
                        "icon": last_item["icon"],
                        "map_embed_url": contact_content_data["map"]["embed_url"],
                        "map_label": contact_content_data["map"]["label"],
                    },
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  Updated map data on: {info_with_map.label}"
                    )
                )

        self.stdout.write(self.style.SUCCESS("\n=== Data population complete! ==="))

    def _print_dry_run(self, contact_page):
        """Print what would be created in dry run mode."""
        self.stdout.write(f"ContactPage: {contact_page.title} (ID: {contact_page.pk})\n")

        self.stdout.write("1. ContactHeader:")
        self.stdout.write(f"   - eyebrow: Get In Touch")
        self.stdout.write(f"   - heading: Let's Build Your Legacy Together.")

        self.stdout.write("\n2. ContactContentSection:")
        self.stdout.write(f"   - heading: Contact Information")

        self.stdout.write("\n3. Contact Info Items:")
        self.stdout.write("     * Call Us: +254 712 345 678")
        self.stdout.write("     * Email Us: info@trustbuildurban.co.ke")
        self.stdout.write("     * Visit Us: Riverside Square, Riverside Dr, Nairobi, Kenya")
        self.stdout.write("     * Map: Google Maps embed URL")
