"""
Management command to populate portfolio page sections data from views.py into the database models.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from portfolio.models import (
    PortfolioPage,
    PortfolioHeader,
    PortfolioProjectsSection,
    PortfolioProjectCategory,
    PortfolioProject,
    ProjectImage,
)


class Command(BaseCommand):
    help = "Populate portfolio page sections with data from views.py"

    def add_arguments(self, parser):
        parser.add_argument(
            "--portfolio-id",
            type=int,
            help="ID of the PortfolioPage to populate data for. If not provided, will use the first published PortfolioPage.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be created without making changes.",
        )

    def handle(self, *args, **options):
        portfolio_id = options.get("portfolio_id")
        dry_run = options.get("dry_run", False)

        # Get the PortfolioPage or create one if it doesn't exist
        if portfolio_id:
            try:
                portfolio_page = PortfolioPage.objects.get(pk=portfolio_id)
            except PortfolioPage.DoesNotExist:
                self.stderr.write(
                    self.style.ERROR(f"PortfolioPage with ID {portfolio_id} does not exist.")
                )
                return
        else:
            portfolio_page = PortfolioPage.objects.filter(is_published=True).first()
            if not portfolio_page:
                # Try to get any portfolio page
                portfolio_page = PortfolioPage.objects.first()
                if not portfolio_page:
                    # Create a default PortfolioPage
                    self.stdout.write(self.style.WARNING("No PortfolioPage found. Creating a default PortfolioPage..."))
                    portfolio_page = PortfolioPage.objects.create(
                        title="Portfolio",
                        slug="portfolio",
                        is_published=True,
                        meta_title="Our Portfolio | TrustBuild Urban",
                        meta_description="Explore our architectural masterpieces across Nairobi and Kiambu."
                    )
                    self.stdout.write(self.style.SUCCESS(f"Created PortfolioPage: {portfolio_page.title} (ID: {portfolio_page.pk})"))

        self.stdout.write(self.style.SUCCESS(f"Using PortfolioPage: {portfolio_page.title} (ID: {portfolio_page.pk})"))

        if dry_run:
            self._print_dry_run(portfolio_page)
            return

        # Data from views.py
        portfolio_header_data = {
            "heading": "Our Portfolio",
            "description": "A showcase of architectural brilliance and construction precision across Nairobi, Kiambu, and beyond.",
        }

        portfolio_projects_data = {
            "filters": ["All", "Ongoing", "Luxury", "Family Home", "Villa", "Mid-Market"],
            "projects": [
                {
                    "title": "Mountain View Estate",
                    "location": "Kiambu Road, Kiambu",
                    "status": "Ongoing",
                    "description": "A premium gated community featuring modern architectural lines and sustainable materials.",
                    "image_url": "/static/images/build1.jpeg",
                },
                {
                    "title": "The Urban Retreat",
                    "location": "Lavington, Nairobi",
                    "status": "Ongoing",
                    "description": "Sophisticated metropolitan living with an emphasis on privacy and luxury finishes.",
                    "image_url": "/static/images/build2.jpeg",
                },
                {
                    "title": "Azure Heights",
                    "location": "Parklands, Nairobi",
                    "status": "Ongoing",
                    "description": "Contemporary luxury apartments with panoramic city views and world-class amenities.",
                    "image_url": "/static/images/build3.jpeg",
                },
                {
                    "title": "Sunset Ridge",
                    "location": "Ngong, Kajiado",
                    "status": "Ongoing",
                    "description": "Family living redefined with expansive outdoor spaces and modern functional design.",
                    "image_url": "/static/images/build4.jpeg",
                },
                {
                    "title": "The Heritage Villa",
                    "location": "Tigoni, Kiambu",
                    "status": "Ongoing",
                    "description": "A timeless blend of classical architectural elements and contemporary luxury.",
                    "image_url": "/static/images/build5.jpeg",
                },
                {
                    "title": "Savanna Heights",
                    "location": "Runda, Nairobi",
                    "status": "Ongoing",
                    "description": "Exclusive villa development with seamless indoor-outdoor living spaces.",
                    "image_url": "/static/images/build6.jpeg",
                },
            ],
        }

        # Create the sections
        with transaction.atomic():
            # 1. Create or Update Portfolio Header
            header, created = PortfolioHeader.objects.update_or_create(
                portfolio_page=portfolio_page,
                defaults={
                    "heading": portfolio_header_data["heading"],
                    "description": portfolio_header_data["description"],
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} PortfolioHeader (ID: {header.pk})"
                )
            )

            # 2. Create or Update Portfolio Projects Section
            projects_section, created = PortfolioProjectsSection.objects.update_or_create(
                portfolio_page=portfolio_page,
                defaults={
                    "learn_more_text": "Learn More",
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} PortfolioProjectsSection (ID: {projects_section.pk})"
                )
            )

            # Create Categories (Filters)
            for idx, category_name in enumerate(portfolio_projects_data["filters"]):
                category, created = PortfolioProjectCategory.objects.update_or_create(
                    projects_section=projects_section,
                    name=category_name,
                    defaults={
                        "order": idx + 1,
                    },
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  {'Created' if created else 'Updated'} Category: {category.name}"
                    )
                )

            # Create Projects
            for idx, project_data in enumerate(portfolio_projects_data["projects"]):
                project, created = PortfolioProject.objects.update_or_create(
                    projects_section=projects_section,
                    title=project_data["title"],
                    defaults={
                        "location": project_data["location"],
                        "status": project_data["status"],
                        "description": project_data["description"],
                        "order": idx + 1,
                    },
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  {'Created' if created else 'Updated'} Project: {project.title}"
                    )
                )

                # Create Project Image
                image, created = ProjectImage.objects.update_or_create(
                    project=project,
                    is_cover=True,
                    defaults={
                        "image_url": project_data["image_url"],
                    },
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"    {'Created' if created else 'Updated'} Cover Image for: {project.title}"
                    )
                )

        self.stdout.write(self.style.SUCCESS("\n=== Data population complete! ==="))

    def _print_dry_run(self, portfolio_page):
        """Print what would be created in dry run mode."""
        self.stdout.write(f"PortfolioPage: {portfolio_page.title} (ID: {portfolio_page.pk})\n")

        self.stdout.write("1. PortfolioHeader:")
        self.stdout.write(f"   - heading: Our Portfolio")
        self.stdout.write(f"   - description: A showcase of architectural brilliance...")

        self.stdout.write("\n2. PortfolioProjectsSection:")
        self.stdout.write(f"   - learn_more_text: Learn More")
        self.stdout.write("   - Categories:")
        for i, cat in enumerate(["All", "Ongoing", "Luxury", "Family Home", "Villa", "Mid-Market"]):
            self.stdout.write(f"     * {cat}")
        self.stdout.write("   - Projects:")
        projects = ["Mountain View Estate", "The Urban Retreat", "Azure Heights", 
                    "Sunset Ridge", "The Heritage Villa", "Savanna Heights"]
        for proj in projects:
            self.stdout.write(f"     * {proj}")
