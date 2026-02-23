"""
Management command to populate homepage sections data from views.py into the database models.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from homepage.models import (
    HomePage,
    HeroSection,
    Stats,
    StatsSection,
    ClientReview,
    DiasporaSection,
    DiasporaChallenge,
    FeaturesSection,
    Feature,
    StepsSection,
    Step,
    ServicesSection,
    Service,
    NewsletterSection,
)
from pages.models import Button


class Command(BaseCommand):
    help = "Populate homepage sections with data from views.py"

    def add_arguments(self, parser):
        parser.add_argument(
            "--homepage-id",
            type=int,
            help="ID of the HomePage to populate data for. If not provided, will use the first published HomePage.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be created without making changes.",
        )

    def handle(self, *args, **options):
        homepage_id = options.get("homepage_id")
        dry_run = options.get("dry_run", False)

        # Get the HomePage
        if homepage_id:
            try:
                homepage = HomePage.objects.get(pk=homepage_id)
            except HomePage.DoesNotExist:
                self.stderr.write(
                    self.style.ERROR(f"HomePage with ID {homepage_id} does not exist.")
                )
                return
        else:
            homepage = HomePage.objects.filter(is_published=True).first()
            if not homepage:
                # Try to get any homepage
                homepage = HomePage.objects.first()
                if not homepage:
                    self.stderr.write(self.style.ERROR("No HomePage found."))
                    return

        self.stdout.write(self.style.SUCCESS(f"Using HomePage: {homepage.title} (ID: {homepage.pk})"))

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN MODE - No changes will be made."))

        # Data from views.py
        hero_data = {
            "tagline": "Building Diaspora Dreams",
            "heading_main": "Find your Best",
            "heading_highlight": "Smart",
            "heading_suffix": "Real Estate.",
            "description": "TrustBuildUrban is a real estate solution that gives you the local scoop on homes in Kenya, backed by corporate transparency and elite design.",
            "cta_primary_text": "Get Started",
            "cta_secondary_text": "Watch video",
            "company_name": "TrustBuild",
            "company_location": "Nairobi, Kenya",
            "verified_text": "Verified",
            "live_tracking_text": "Live Project Tracking",
            "show_verified_badge": True,
            "show_live_tracking": True,
            "stats": {
                "happy_customers": {"value": "5032", "label": "Happy Customers"},
                "property_sales": {"value": "6700+", "label": "Property Sales"},
                "award_winning": {"value": "205+", "label": "Award Winning"},
            },
        }

        stats_section_data = {
            "quote_text": "Integrity and innovation in every structure we touch. Engineering excellence from the ground up.",
            "landmark_projects_value": "850",
            "landmark_projects_label_text": "Landmark Projects",
            "client_reviews": {
                "rating": 5,
                "total_reviews": "12,000+",
                "label_text": "Client Reviews",
                "button_text": "Discover Excellence",
                "button_link": "#",
            },
        }

        diaspora_section_data = {
            "eyebrow": "The Diaspora Challenge",
            "heading": "Building in Kenya should not be a gamble.",
            "challenges": [
                {
                    "title": "Fear of Misused Funds",
                    "description": "Money sent for building being diverted for other family uses or personal gain.",
                },
                {
                    "title": "Lack of Supervision",
                    "description": "No one reliable to check site progress and quality on a daily basis.",
                },
                {
                    "title": "Project Delays",
                    "description": "Timelines stretching for years with no clear explanation or end date.",
                },
                {
                    "title": "Poor Workmanship",
                    "description": "Low-quality materials used despite paying premium prices.",
                },
                {
                    "title": "Legal Risks",
                    "description": "Issues with titles, county permits, and unlicensed contractors.",
                },
            ],
            "attribution": "TrustBuildUrban was founded to replace fear with structured, world-class building standards.",
            "featured_project": {
                "label": "Featured Project",
                "title": "The Grand Residence, Runda",
                "image_url": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?q=80&w=870&auto=format&fit=crop",
            },
        }

        features_section_data = {
            "eyebrow": "The TrustBuildUrban Standard",
            "heading": "Why Hundreds of Diaspora Families Trust Us",
            "features": [
                {
                    "title": "Transparent Cost Breakdowns",
                    "description": "Detailed bill of quantities before a single stone is moved.",
                    "icon_path": """
                    <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-file-text-icon lucide-file-text"><path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"/><path d="M14 2v5a1 1 0 0 0 1 1h5"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/></svg>
                    """,
                },
                {
                    "title": "Stage-Based Payments",
                    "description": "Pay only for completed and verified construction milestones.",
                    "icon_path": """ <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-calendar-check-icon lucide-calendar-check"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/><path d="m9 16 2 2 4-4"/></svg>
                    """,
                },
                {
                    "title": "Weekly Photo & Video Updates",
                    "description": "Regular high-definition visual reporting of your site progress.",
                    "icon_path": """
                        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-eye-icon lucide-eye"><path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"/><circle cx="12" cy="12" r="3"/></svg>
                    """,
                },
                {
                    "title": "Virtual Site Walkthroughs",
                    "description": "Live video tours allowing you to inspect every corner remotely.",
                    "icon_path": """
                    <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-shield-check-icon lucide-shield-check"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/></svg>
                    """,
                },
                {
                    "title": "Legally Documented Contracts",
                    "description": "Every project is backed by enforceable stamped legal agreements.",
                    "icon_path": """
                       <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-file-badge-icon lucide-file-badge"><path d="M13 22h5a2 2 0 0 0 2-2V8a2.4 2.4 0 0 0-.706-1.706l-3.588-3.588A2.4 2.4 0 0 0 14 2H6a2 2 0 0 0-2 2v3.3"/><path d="M14 2v5a1 1 0 0 0 1 1h5"/><path d="m7.69 16.479 1.29 4.88a.5.5 0 0 1-.698.591l-1.843-.849a1 1 0 0 0-.879.001l-1.846.85a.5.5 0 0 1-.692-.593l1.29-4.88"/><circle cx="6" cy="14" r="3"/></svg>
                    """,
                },
                {
                    "title": "Quality Assurance Team",
                    "description": "Independent engineers verifying work against Kenyan building codes.",
                    "icon_path": """
                   <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-badge-check-icon lucide-badge-check"><path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"/><path d="m9 12 2 2 4-4"/></svg>
                    """,
                },
            ],
        }

        steps_section_data = {
            "eyebrow": "Transparent Execution",
            "heading": "Our 7-Step Architectural Journey",
            "description": "A meticulously structured process from initial concept to the day we hand over your keys.",
            "steps": [
                {"title": "Virtual Consultation", "description": "Define goals vision via high-level Zoom/Meet session."},
                {"title": "Budget Planning", "description": "Detailed cost estimation and financial structuring."},
                {"title": "Land Verification", "description": "Legal search and site analysis for clean title."},
                {"title": "Architectural Design", "description": "Collaborative drafting of blueprints and 3D visuals."},
                {"title": "Approvals & Documentation", "description": "Handling all NCA and County government permits."},
                {"title": "Structured Construction", "description": "Phased build with weekly milestones and reports."},
                {"title": "Handover & Warranty", "description": "Final inspection key handover and support."},
            ],
        }

        services_section_data = {
            "subtitle": "Our Specializations",
            "heading": "Elite Engineering & Architectural Excellence",
            "services": [
                {
                    "icon": """
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                    class="lucide w-10 h-10" aria-hidden="true">
                    <path d="m2 22 1-1h3l9-9"></path><path d="M14 2h.01"></path><path d="M7 2h.01"></path><path d="M3.5 15.5 8 11"></path><path d="m5 11 3 3"></path><path d="M19 13.5v7a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2h7"></path><path d="M11 2h.01"></path><path d="m17 2 3.3 3.3c.39.39.39 1.02 0 1.41L17 10"></path><path d="M13 2v8"></path>
                  </svg>
                    """,
                    "title": "Innovative Civil Engineering",
                    "description": "Our engineering team focuses on structural integrity and future-proof solutions. We use advanced BIM modeling to ensure every beam and column is optimized for safety and efficiency.",
                    "expertise": "Structural Analysis, Foundation Design, Retaining Walls, Drainage Systems",
                },
                {
                    "icon": """
                     <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                class="lucide w-10 h-10" aria-hidden="true">
                <path d="M3 14h18"></path><path d="M3 18h18"></path><path d="M4 10V4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v6"></path><path d="m12 2 4 4-4 4-4-4 4-4z"></path>
              </svg>
                    """,
                    "title": "Architectural Masterpieces",
                    "description": "We believe architecture should tell a story. From ultra-modern villas to sustainable commercial hubs, our designs balance aesthetics with functionality and cultural context.",
                    "expertise": "Conceptual Design, Interior Architecture, Landscape Architecture, Sustainable Architecture",
                },
            ],
        }

        newsletter_data = {
            "heading": "Free Diaspora Home Building Guide",
            "description": "Download our comprehensive manual on navigating land laws, approvals, and construction costs in Kenya from abroad.",
            "cta_text": "GET THE GUIDE",
            "placeholder": "Enter your email",
        }

        if dry_run:
            self.stdout.write("\n=== DRY RUN - Would create the following ===\n")
            self._print_dry_run(
                homepage,
                hero_data,
                stats_section_data,
                diaspora_section_data,
                features_section_data,
                steps_section_data,
                services_section_data,
                newsletter_data,
            )
            return

        # Create the sections
        with transaction.atomic():
            # 0. Create or Update Hero Section
            hero_section, created = HeroSection.objects.update_or_create(
                homepage=homepage,
                defaults={
                    "tagline": hero_data["tagline"],
                    "heading_main": hero_data["heading_main"],
                    "heading_highlight": hero_data["heading_highlight"],
                    "heading_suffix": hero_data["heading_suffix"],
                    "description": hero_data["description"],
                    "company_name": hero_data["company_name"],
                    "company_location": hero_data["company_location"],
                    "verified_text": hero_data["verified_text"],
                    "live_tracking_text": hero_data["live_tracking_text"],
                    "show_verified_badge": hero_data["show_verified_badge"],
                    "show_live_tracking": hero_data["show_live_tracking"],
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} HeroSection (ID: {hero_section.pk})"
                )
            )

            # Create Hero Stats
            for idx, (key, stat_data) in enumerate(hero_data["stats"].items()):
                stat, created = Stats.objects.update_or_create(
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

            # 0b. Create Stats Section
            stats_section, created = StatsSection.objects.update_or_create(
                homepage=homepage,
                defaults={
                    "quote_text": stats_section_data["quote_text"],
                    "landmark_projects_value": stats_section_data["landmark_projects_value"],
                    "landmark_projects_label_text": stats_section_data["landmark_projects_label_text"],
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} StatsSection (ID: {stats_section.pk})"
                )
            )

            # Create Client Reviews
            review_data = stats_section_data["client_reviews"]
            review, created = ClientReview.objects.update_or_create(
                stats_section=stats_section,
                defaults={
                    "rating": review_data["rating"],
                    "total_reviews": review_data["total_reviews"],
                    "label_text": review_data["label_text"],
                    "button_text": review_data["button_text"],
                    "button_link": review_data["button_link"],
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} ClientReview: {review.label_text}"
                )
            )

            # 1. Create Diaspora Section
            diaspora_section, created = DiasporaSection.objects.update_or_create(
                homepage=homepage,
                defaults={
                    "eyebrow": diaspora_section_data["eyebrow"],
                    "heading": diaspora_section_data["heading"],
                    "attribution": diaspora_section_data["attribution"],
                    "featured_label": diaspora_section_data["featured_project"]["label"],
                    "featured_title": diaspora_section_data["featured_project"]["title"],
                    "featured_image_url": diaspora_section_data["featured_project"]["image_url"],
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} DiasporaSection (ID: {diaspora_section.pk})"
                )
            )

            # Create Diaspora Challenges
            for idx, challenge_data in enumerate(diaspora_section_data["challenges"]):
                challenge, created = DiasporaChallenge.objects.update_or_create(
                    diaspora_section=diaspora_section,
                    title=challenge_data["title"],
                    defaults={
                        "description": challenge_data["description"],
                        "order": idx + 1,
                    },
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  {'Created' if created else 'Updated'} DiasporaChallenge: {challenge.title}"
                    )
                )

            # 2. Create Features Section
            features_section, created = FeaturesSection.objects.update_or_create(
                homepage=homepage,
                defaults={
                    "eyebrow": features_section_data["eyebrow"],
                    "heading": features_section_data["heading"],
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} FeaturesSection (ID: {features_section.pk})"
                )
            )

            # Create Features
            for idx, feature_data in enumerate(features_section_data["features"]):
                feature, created = Feature.objects.update_or_create(
                    features_section=features_section,
                    title=feature_data["title"],
                    defaults={
                        "description": feature_data["description"],
                        "icon_path": feature_data["icon_path"],
                        "order": idx + 1,
                    },
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  {'Created' if created else 'Updated'} Feature: {feature.title}"
                    )
                )

            # 3. Create Steps Section
            steps_section, created = StepsSection.objects.update_or_create(
                homepage=homepage,
                defaults={
                    "eyebrow": steps_section_data["eyebrow"],
                    "heading": steps_section_data["heading"],
                    "description": steps_section_data["description"],
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} StepsSection (ID: {steps_section.pk})"
                )
            )

            # Create Steps
            for idx, step_data in enumerate(steps_section_data["steps"]):
                step, created = Step.objects.update_or_create(
                    steps_section=steps_section,
                    title=step_data["title"],
                    defaults={
                        "description": step_data["description"],
                        "order": idx + 1,
                    },
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  {'Created' if created else 'Updated'} Step: {step.title}"
                    )
                )

            # 4. Create Services Section
            services_section, created = ServicesSection.objects.update_or_create(
                homepage=homepage,
                defaults={
                    "subtitle": services_section_data["subtitle"],
                    "heading": services_section_data["heading"],
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} ServicesSection (ID: {services_section.pk})"
                )
            )

            # Create Services
            for idx, service_data in enumerate(services_section_data["services"]):
                service, created = Service.objects.update_or_create(
                    services_section=services_section,
                    title=service_data["title"],
                    defaults={
                        "description": service_data["description"],
                        "icon": service_data["icon"],
                        "expertise": service_data["expertise"],
                        "order": idx + 1,
                    },
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  {'Created' if created else 'Updated'} Service: {service.title}"
                    )
                )

            # 5. Create Newsletter Section
            newsletter_section, created = NewsletterSection.objects.update_or_create(
                homepage=homepage,
                defaults={
                    "heading": newsletter_data["heading"],
                    "description": newsletter_data["description"],
                    "placeholder": newsletter_data["placeholder"],
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} NewsletterSection (ID: {newsletter_section.pk})"
                )
            )
            # Note: Newsletter uses an email input form, not a typical button
            # The CTA text is stored in the placeholder field for the form

        self.stdout.write(self.style.SUCCESS("\n=== Data population complete! ==="))

    def _print_dry_run(
        self,
        homepage,
        hero_data,
        stats_section_data,
        diaspora_data,
        features_data,
        steps_data,
        services_data,
        newsletter_data,
    ):
        """Print what would be created in dry run mode."""
        self.stdout.write(f"HomePage: {homepage.title} (ID: {homepage.pk})\n")

        self.stdout.write("0. HeroSection:")
        self.stdout.write(f"   - tagline: {hero_data['tagline']}")
        self.stdout.write(f"   - heading_main: {hero_data['heading_main']}")
        self.stdout.write(f"   - heading_highlight: {hero_data['heading_highlight']}")
        self.stdout.write(f"   - heading_suffix: {hero_data['heading_suffix']}")
        self.stdout.write(f"   - description: {hero_data['description']}")
        self.stdout.write(f"   - company_name: {hero_data['company_name']}")
        self.stdout.write(f"   - company_location: {hero_data['company_location']}")
        self.stdout.write("   - Stats:")
        for key, stat in hero_data["stats"].items():
            self.stdout.write(f"     * {stat['label']}: {stat['value']}")

        self.stdout.write("\n0b. StatsSection:")
        self.stdout.write(f"   - quote_text: {stats_section_data['quote_text'][:50]}...")
        self.stdout.write(f"   - landmark_projects: {stats_section_data['landmark_projects_value']}")
        self.stdout.write("   - ClientReview:")
        self.stdout.write(f"     * rating: {stats_section_data['client_reviews']['rating']}")
        self.stdout.write(f"     * total_reviews: {stats_section_data['client_reviews']['total_reviews']}")

        self.stdout.write("\n1. DiasporaSection:")
        self.stdout.write(f"   - eyebrow: {diaspora_data['eyebrow']}")
        self.stdout.write(f"   - heading: {diaspora_data['heading']}")
        self.stdout.write(f"   - attribution: {diaspora_data['attribution']}")
        self.stdout.write(f"   - featured_project: {diaspora_data['featured_project']['title']}")
        self.stdout.write("   - Challenges:")
        for c in diaspora_data["challenges"]:
            self.stdout.write(f"     * {c['title']}")

        self.stdout.write("\n2. FeaturesSection:")
        self.stdout.write(f"   - eyebrow: {features_data['eyebrow']}")
        self.stdout.write(f"   - heading: {features_data['heading']}")
        self.stdout.write("   - Features:")
        for f in features_data["features"]:
            self.stdout.write(f"     * {f['title']}")

        self.stdout.write("\n3. StepsSection:")
        self.stdout.write(f"   - eyebrow: {steps_data['eyebrow']}")
        self.stdout.write(f"   - heading: {steps_data['heading']}")
        self.stdout.write("   - Steps:")
        for s in steps_data["steps"]:
            self.stdout.write(f"     * {s['title']}")

        self.stdout.write("\n4. ServicesSection:")
        self.stdout.write(f"   - subtitle: {services_data['subtitle']}")
        self.stdout.write(f"   - heading: {services_data['heading']}")
        self.stdout.write("   - Services:")
        for s in services_data["services"]:
            self.stdout.write(f"     * {s['title']}")

        self.stdout.write("\n5. NewsletterSection:")
        self.stdout.write(f"   - heading: {newsletter_data['heading']}")
        self.stdout.write(f"   - description: {newsletter_data['description']}")
        self.stdout.write(f"   - cta_text: {newsletter_data['cta_text']}")
        self.stdout.write(f"   - placeholder: {newsletter_data['placeholder']}")
