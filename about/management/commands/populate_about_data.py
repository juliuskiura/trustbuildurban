"""
Management command to populate about page sections data from views.py into the database models.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from about.models import (
    AboutPage,
    HeroSection,
    Stat,
    CorePillarsSection,
    Pillar,
)


class Command(BaseCommand):
    help = "Populate about page sections with data from views.py"

    def add_arguments(self, parser):
        parser.add_argument(
            "--about-id",
            type=int,
            help="ID of the AboutPage to populate data for. If not provided, will use the first published AboutPage.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be created without making changes.",
        )

    def handle(self, *args, **options):
        about_id = options.get("about_id")
        dry_run = options.get("dry_run", False)

        # Get the AboutPage or create one if it doesn't exist
        if about_id:
            try:
                about_page = AboutPage.objects.get(pk=about_id)
            except AboutPage.DoesNotExist:
                self.stderr.write(
                    self.style.ERROR(f"AboutPage with ID {about_id} does not exist.")
                )
                return
        else:
            about_page = AboutPage.objects.filter(is_published=True).first()
            if not about_page:
                # Try to get any about page
                about_page = AboutPage.objects.first()
                if not about_page:
                    # Create a default AboutPage
                    self.stdout.write(self.style.WARNING("No AboutPage found. Creating a default AboutPage..."))
                    about_page = AboutPage.objects.create(
                        title="About Us",
                        slug="about",
                        is_published=True,
                        meta_title="About | TrustBuild Urban",
                        meta_description="Learn about our mission of radical transparency and excellence in construction."
                    )
                    self.stdout.write(self.style.SUCCESS(f"Created AboutPage: {about_page.title} (ID: {about_page.pk})"))

        self.stdout.write(self.style.SUCCESS(f"Using AboutPage: {about_page.title} (ID: {about_page.pk})"))

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN MODE - No changes will be made."))

        # Data from views.py
        hero_section_data = {
            "eyebrow": "Our Story",
            "heading": "Excellence in Construction, Built on Trust.",
            "description": "Founded on the principle of radical transparency, TrustBuild Urban has become the premier choice for Kenyans living abroad and local high-end homeowners. We recognized a massive gap in the market: the lack of corporate accountability in residential construction. Our mission is to provide a seamless, stress-free building experience where quality is never compromised, and every shilling is accounted for. We don't just build houses; we build legacies.",
            "image_url": "https://images.unsplash.com/photo-1541914590372-e01d89758e5a?auto=format&fit=crop&q=80&w=1200",
            "image_alt": "Architecture Team",
            "quote": "Transparency isn't a buzzword; it's our core architecture.",
            "stats": [
                {"value": "10+", "label": "Years Experience"},
                {"value": "150+", "label": "Projects Completed"},
            ],
        }

        pillars_section_data = {
            "eyebrow": "The TrustBuild Standards",
            "heading": "Our Core Pillars",
            "pillars": [
                {
                    "title": "Uncompromising Quality",
                    "description": "We source premium materials and employ master craftsmen to ensure every finish is world-class.",
                    "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-award w-8 h-8" aria-hidden="true"><path d="m15.477 12.89 1.515 8.526a.5.5 0 0 1-.81.47l-3.58-2.687a1 1 0 0 0-1.197 0l-3.586 2.686a.5.5 0 0 1-.81-.469l1.514-8.526"></path><circle cx="12" cy="8" r="6"></circle></svg>""",
                },
                {
                    "title": "Client Partnership",
                    "description": "We act as your local eyes and ears, treating your investment with the same care as our own.",
                    "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-users w-8 h-8" aria-hidden="true"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><path d="M16 3.128a4 4 0 0 1 0 7.744"></path><path d="M22 21v-2a4 4 0 0 0-3-3.87"></path><circle cx="9" cy="7" r="4"></circle></svg>""",
                },
                {
                    "title": "Ethical Conduct",
                    "description": "From legal land acquisition to labor management, we operate with absolute integrity.",
                    "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-circle-check-big w-8 h-8" aria-hidden="true"><path d="M21.801 10A10 10 0 1 1 17 3.335"></path><path d="m9 11 3 3L22 4"></path></svg>""",
                },
            ],
        }

        if dry_run:
            self._print_dry_run(about_page, hero_section_data, pillars_section_data)
            return

        # Create the sections
        with transaction.atomic():
            # 1. Create or Update Hero Section
            hero_section, created = HeroSection.objects.update_or_create(
                about_page=about_page,
                defaults={
                    "eyebrow": hero_section_data["eyebrow"],
                    "heading": hero_section_data["heading"],
                    "description": hero_section_data["description"],
                    "image_url": hero_section_data["image_url"],
                    "image_alt": hero_section_data["image_alt"],
                    "quote": hero_section_data["quote"],
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} HeroSection (ID: {hero_section.pk})"
                )
            )

            # Create Stats (attached to HeroSection)
            for idx, stat_data in enumerate(hero_section_data["stats"]):
                stat, created = Stat.objects.update_or_create(
                    hero_section=hero_section,
                    label=stat_data["label"],
                    defaults={
                        "value": stat_data["value"],
                        "order": idx + 1,
                    },
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  {'Created' if created else 'Updated'} Stat: {stat.label}"
                    )
                )

            # 2. Create or Update CorePillars Section
            pillars_section, created = CorePillarsSection.objects.update_or_create(
                about_page=about_page,
                defaults={
                    "eyebrow": pillars_section_data["eyebrow"],
                    "heading": pillars_section_data["heading"],
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} CorePillarsSection (ID: {pillars_section.pk})"
                )
            )

            # Create Pillars
            for idx, pillar_data in enumerate(pillars_section_data["pillars"]):
                pillar, created = Pillar.objects.update_or_create(
                    core_pillars_section=pillars_section,
                    title=pillar_data["title"],
                    defaults={
                        "description": pillar_data["description"],
                        "icon": pillar_data["icon"],
                        "order": idx + 1,
                    },
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  {'Created' if created else 'Updated'} Pillar: {pillar.title}"
                    )
                )

        self.stdout.write(self.style.SUCCESS("\n=== Data population complete! ==="))

    def _print_dry_run(self, about_page, hero_data, pillars_data):
        """Print what would be created in dry run mode."""
        self.stdout.write(f"AboutPage: {about_page.title} (ID: {about_page.pk})\n")

        self.stdout.write("1. HeroSection:")
        self.stdout.write(f"   - eyebrow: {hero_data['eyebrow']}")
        self.stdout.write(f"   - heading: {hero_data['heading']}")
        self.stdout.write(f"   - quote: {hero_data['quote']}")
        self.stdout.write("   - Stats:")
        for stat in hero_data["stats"]:
            self.stdout.write(f"     * {stat['label']}: {stat['value']}")

        self.stdout.write("\n2. CorePillarsSection:")
        self.stdout.write(f"   - eyebrow: {pillars_data['eyebrow']}")
        self.stdout.write(f"   - heading: {pillars_data['heading']}")
        self.stdout.write("   - Pillars:")
        for pillar in pillars_data["pillars"]:
            self.stdout.write(f"     * {pillar['title']}")
