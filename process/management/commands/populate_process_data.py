"""
Management command to populate process page sections data from views.py into the database models.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.contenttypes.models import ContentType

from process.models import (
    ProcessPage,
    HeaderSection,
    ProcessSteps,
    ProcessStep,
    ProcessCTA,
)
from pages.models import Button


class Command(BaseCommand):
    help = "Populate process page sections with data from views.py"

    def add_arguments(self, parser):
        parser.add_argument(
            "--process-id",
            type=int,
            help="ID of the ProcessPage to populate data for. If not provided, will use the first published ProcessPage.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be created without making changes.",
        )

    def handle(self, *args, **options):
        process_id = options.get("process_id")
        dry_run = options.get("dry_run", False)

        # Get the ProcessPage or create one if it doesn't exist
        if process_id:
            try:
                process_page = ProcessPage.objects.get(pk=process_id)
            except ProcessPage.DoesNotExist:
                self.stderr.write(
                    self.style.ERROR(f"ProcessPage with ID {process_id} does not exist.")
                )
                return
        else:
            process_page = ProcessPage.objects.filter(is_published=True).first()
            if not process_page:
                # Try to get any process page
                process_page = ProcessPage.objects.first()
                if not process_page:
                    # Create a default ProcessPage
                    self.stdout.write(self.style.WARNING("No ProcessPage found. Creating a default ProcessPage..."))
                    process_page = ProcessPage.objects.create(
                        title="Our Process",
                        slug="process",
                        is_published=True,
                        meta_title="Our Process | TrustBuild Urban",
                        meta_description="Discover our 7-step roadmap to predictable construction results in Kenya."
                    )
                    self.stdout.write(self.style.SUCCESS(f"Created ProcessPage: {process_page.title} (ID: {process_page.pk})"))

        self.stdout.write(self.style.SUCCESS(f"Using ProcessPage: {process_page.title} (ID: {process_page.pk})"))

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN MODE - No changes will be made."))

        # Data from views.py
        header_data = {
            "eyebrow": "How We Work",
            "heading": "The 7-Step TrustBuild Roadmap",
            "description": "Construction in Kenya doesn't have to be chaotic. We use a standardized corporate workflow to ensure predictable results every time.",
        }

        process_steps_data = {
            "quality_gate_label": "Quality Gate",
            "quality_gate_text": "This stage must be signed off by both our lead engineer and the client before proceeding.",
            "steps": [
                {"title": "Consultation", "description": "Brainstorming and roadmap development."},
                {"title": "Feasibility", "description": "Site visits and legal title verification."},
                {"title": "Concept", "description": "Architectural designs and floor planning."},
                {"title": "Approvals", "description": "NCA and County government legal sign-offs."},
                {"title": "Contracts", "description": "Bill of quantities and fixed-price agreements."},
                {"title": "Construction", "description": "Structured building with live video updates."},
                {"title": "Handover", "description": "Quality verification and key ceremony."},
            ],
        }

        cta_data = {
            "heading": "Ready to take step one?",
            "button_text": "Book Initial Consultation",
            "button_link": "#contact",
        }

        if dry_run:
            self._print_dry_run(process_page, header_data, process_steps_data, cta_data)
            return

        # Create the sections
        with transaction.atomic():
            # 1. Create or Update Header Section
            header_section, created = HeaderSection.objects.update_or_create(
                process_page=process_page,
                defaults={
                    "eyebrow": header_data["eyebrow"],
                    "heading": header_data["heading"],
                    "description": header_data["description"],
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} HeaderSection (ID: {header_section.pk})"
                )
            )

            # 2. Create or Update Process Steps Section
            steps_section, created = ProcessSteps.objects.update_or_create(
                process_page=process_page,
                defaults={
                    "quality_gate_label": process_steps_data["quality_gate_label"],
                    "quality_gate_text": process_steps_data["quality_gate_text"],
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} ProcessSteps (ID: {steps_section.pk})"
                )
            )

            # Create Process Steps
            for idx, step_data in enumerate(process_steps_data["steps"]):
                step, created = ProcessStep.objects.update_or_create(
                    process_steps=steps_section,
                    title=step_data["title"],
                    defaults={
                        "description": step_data["description"],
                        "order": idx + 1,
                    },
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  {'Created' if created else 'Updated'} ProcessStep: {step.title}"
                    )
                )

            # 3. Create or Update Process CTA Section
            cta_section, created = ProcessCTA.objects.update_or_create(
                process_page=process_page,
                defaults={
                    "heading": cta_data["heading"],
                    "button_text": cta_data["button_text"],
                    "button_link": cta_data["button_link"],
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} ProcessCTA (ID: {cta_section.pk})"
                )
            )

        self.stdout.write(self.style.SUCCESS("\n=== Data population complete! ==="))

    def _print_dry_run(self, process_page, header_data, steps_data, cta_data):
        """Print what would be created in dry run mode."""
        self.stdout.write(f"ProcessPage: {process_page.title} (ID: {process_page.pk})\n")

        self.stdout.write("1. HeaderSection:")
        self.stdout.write(f"   - eyebrow: {header_data['eyebrow']}")
        self.stdout.write(f"   - heading: {header_data['heading']}")
        self.stdout.write(f"   - description: {header_data['description'][:50]}...")

        self.stdout.write("\n2. ProcessSteps:")
        self.stdout.write(f"   - quality_gate_label: {steps_data['quality_gate_label']}")
        self.stdout.write(f"   - quality_gate_text: {steps_data['quality_gate_text'][:50]}...")
        self.stdout.write("   - Steps:")
        for step in steps_data["steps"]:
            self.stdout.write(f"     * {step['title']}")

        self.stdout.write("\n3. ProcessCTA:")
        self.stdout.write(f"   - heading: {cta_data['heading']}")
        self.stdout.write(f"   - button_text: {cta_data['button_text']}")
        self.stdout.write(f"   - button_link: {cta_data['button_link']}")
