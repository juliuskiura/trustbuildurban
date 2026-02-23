"""
Management command to populate services page sections data from views.py into the database models.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from services.models import (
    ServicePage,
    ServicesHeader,
    ServicesListSection,
    Service,
)


class Command(BaseCommand):
    help = "Populate services page sections with data from views.py"

    def add_arguments(self, parser):
        parser.add_argument(
            "--services-id",
            type=int,
            help="ID of the ServicePage to populate data for. If not provided, will use the first published ServicePage.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be created without making changes.",
        )

    def handle(self, *args, **options):
        services_id = options.get("services_id")
        dry_run = options.get("dry_run", False)

        # Get the ServicePage or create one if it doesn't exist
        if services_id:
            try:
                service_page = ServicePage.objects.get(pk=services_id)
            except ServicePage.DoesNotExist:
                self.stderr.write(
                    self.style.ERROR(f"ServicePage with ID {services_id} does not exist.")
                )
                return
        else:
            service_page = ServicePage.objects.filter(is_published=True).first()
            if not service_page:
                # Try to get any service page
                service_page = ServicePage.objects.first()
                if not service_page:
                    # Create a default ServicePage
                    self.stdout.write(self.style.WARNING("No ServicePage found. Creating a default ServicePage..."))
                    service_page = ServicePage.objects.create(
                        title="Services",
                        slug="services",
                        is_published=True,
                        meta_title="Our Services | TrustBuild Urban",
                        meta_description="Specialized solutions in construction, project management, and structural engineering by TrustBuild Urban."
                    )
                    self.stdout.write(self.style.SUCCESS(f"Created ServicePage: {service_page.title} (ID: {service_page.pk})"))

        self.stdout.write(self.style.SUCCESS(f"Using ServicePage: {service_page.title} (ID: {service_page.pk})"))

        if dry_run:
            self._print_dry_run(service_page)
            return

        # Data from views.py
        services_header_data = {
            "eyebrow": "What We Do",
            "heading": "Specialized Solutions for Discerning Clients.",
            "description": "From the first site visit to the final coat of paint, we manage the complexities of construction so you don't have to.",
        }

        services_list_data = {
            "learn_more_text": "Learn More",
            "services": [
                {
                    "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-globe w-10 h-10" aria-hidden="true"><circle cx="12" cy="12" r="10"></circle><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"></path><path d="M2 12h20"></path></svg>""",
                    "title": "Consultancy",
                    "description": "Expert advice for your building project. We handle all the heavy lifting, ensuring your project meets both local regulations and international standards.",
                    "image_url": "https://images.unsplash.com/photo-1541914590372-e01d89758e5a?auto=format&fit=crop&q=80&w=1200",
                    "link": "/contact",
                },
                {
                    "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-house w-10 h-10" aria-hidden="true"><path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"></path><path d="M3 10a2 2 0 0 1 .709-1.528l7-6a2 2 0 0 1 2.582 0l7 6A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path></svg>""",
                    "title": "Construction",
                    "description": "Quality builds you can trust. We manage master craftsmen and premium materials to ensure your legacy is built to the highest possible standards.",
                    "image_url": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&q=80&w=1200",
                    "link": "/contact",
                },
                {
                    "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-settings w-10 h-10" aria-hidden="true"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"></path><circle cx="12" cy="12" r="3"></circle></svg>""",
                    "title": "Project Management",
                    "description": "We manage everything for you. From procurement to labor management, we act as your local eyes and ears, treating your investment with the same care as our own.",
                    "image_url": "https://images.unsplash.com/photo-1541888946425-d81bb19480c5?auto=format&fit=crop&q=80&w=1200",
                    "link": "/contact",
                },
                {
                    "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-search w-10 h-10" aria-hidden="true"><circle cx="11" cy="11" r="8"></circle><path d="m21 21-4.3-4.3"></path></svg>""",
                    "title": "Site Inspection",
                    "description": "Regular checks on your progress. We provide detailed reports and live video updates, ensuring radical transparency throughout the building lifecycle.",
                    "image_url": "https://images.unsplash.com/photo-1531834685032-c34bf0d84c77?auto=format&fit=crop&q=80&w=1200",
                    "link": "/contact",
                },
            ],
        }

        # Create the sections
        with transaction.atomic():
            # 1. Create or Update Services Header
            header, created = ServicesHeader.objects.update_or_create(
                service_page=service_page,
                defaults={
                    "eyebrow": services_header_data["eyebrow"],
                    "heading": services_header_data["heading"],
                    "description": services_header_data["description"],
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} ServicesHeader (ID: {header.pk})"
                )
            )

            # 2. Create or Update Services List Section
            services_section, created = ServicesListSection.objects.update_or_create(
                service_page=service_page,
                defaults={
                    "learn_more_text": services_list_data["learn_more_text"],
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} ServicesListSection (ID: {services_section.pk})"
                )
            )

            # Create Services
            for idx, service_data in enumerate(services_list_data["services"]):
                service, created = Service.objects.update_or_create(
                    services_section=services_section,
                    title=service_data["title"],
                    defaults={
                        "description": service_data["description"],
                        "icon": service_data["icon"],
                        "image_url": service_data["image_url"],
                        "link": service_data.get("link", "/contact"),
                        "order": idx + 1,
                    },
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  {'Created' if created else 'Updated'} Service: {service.title}"
                    )
                )

        self.stdout.write(self.style.SUCCESS("\n=== Data population complete! ==="))

    def _print_dry_run(self, service_page):
        """Print what would be created in dry run mode."""
        self.stdout.write(f"ServicePage: {service_page.title} (ID: {service_page.pk})\n")

        self.stdout.write("1. ServicesHeader:")
        self.stdout.write(f"   - eyebrow: What We Do")
        self.stdout.write(f"   - heading: Specialized Solutions for Discerning Clients.")

        self.stdout.write("\n2. ServicesListSection:")
        self.stdout.write(f"   - learn_more_text: Learn More")
        self.stdout.write("   - Services:")
        services = ["Consultancy", "Construction", "Project Management", "Site Inspection"]
        for svc in services:
            self.stdout.write(f"     * {svc}")
