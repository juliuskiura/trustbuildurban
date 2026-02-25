from django.core.management.base import BaseCommand
from available_homes.models import (
    AvailableHomesPage,
    AvailableHomesHeroSection,
    AvailableHomesCTASection,
    AvailableHome,
)


class Command(BaseCommand):
    help = "Populate available homes with sample data"

    def handle(self, *args, **options):
        self.stdout.write("Creating available homes data...")

        # Create AvailableHomesPage
        page, created = AvailableHomesPage.objects.get_or_create(
            slug="available-homes",
            defaults={
                "title": "Available Homes",
                "is_published": True,
                "show_in_menus": True,
                "menu_order": 4,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created page: {page.title}"))
        else:
            self.stdout.write(f"Page already exists: {page.title}")

        # Create Hero Section
        hero_section, created = AvailableHomesHeroSection.objects.get_or_create(
            available_homes_page=page,
            defaults={
                "title": "Available Homes For Sale",
                "description": "High-quality homes built by TrustBuildUrban for immediate purchase. Move-in ready residences in Kenya's most sought-after neighborhoods.",
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Created hero section"))
        else:
            self.stdout.write("Hero section already exists")

        # Create CTA Section
        cta_section, created = AvailableHomesCTASection.objects.get_or_create(
            available_homes_page=page,
            defaults={
                "title": "Didn't find what you're looking for?",
                "description": "We can design and build a bespoke home specifically for you on your preferred piece of land.",
                "button_text": "LEARN ABOUT CUSTOM BUILD",
                "button_link": "/process/",
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Created CTA section"))
        else:
            self.stdout.write("CTA section already exists")

        # Create sample homes
        homes_data = [
            {
                "title": "The Sapphire Residence",
                "location": "Sigona, Kiambu",
                "price": "KES 45,000,000",
                "beds": 4,
                "baths": 4,
                "sqft": 3200,
                "status": "available",
                "image_url": "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&q=80&w=1200",
                "is_featured": True,
            },
            {
                "title": "Veranda Suites",
                "location": "Migaa, Kiambu",
                "price": "KES 38,500,000",
                "beds": 3,
                "baths": 3,
                "sqft": 2800,
                "status": "under_offer",
                "image_url": "https://images.unsplash.com/photo-1518780664697-55e3ad937233?auto=format&fit=crop&q=80&w=1200",
                "is_featured": False,
            },
            {
                "title": "The Garden Estate",
                "location": "Ruiru, Kiambu",
                "price": "KES 32,000,000",
                "beds": 4,
                "baths": 3,
                "sqft": 2600,
                "status": "available",
                "image_url": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&q=80&w=1200",
                "is_featured": True,
            },
            {
                "title": "Modern Loft Apartments",
                "location": "Kasarani, Nairobi",
                "price": "KES 28,500,000",
                "beds": 3,
                "baths": 2,
                "sqft": 2200,
                "status": "available",
                "image_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&q=80&w=1200",
                "is_featured": False,
            },
            {
                "title": "The Palm Springs",
                "location": "Mombasa Road, Nairobi",
                "price": "KES 55,000,000",
                "beds": 5,
                "baths": 5,
                "sqft": 4500,
                "status": "available",
                "image_url": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&q=80&w=1200",
                "is_featured": True,
            },
            {
                "title": "The Willow Creek",
                "location": "Athi River, Machakos",
                "price": "KES 22,000,000",
                "beds": 3,
                "baths": 2,
                "sqft": 1800,
                "status": "reserved",
                "image_url": "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&q=80&w=1200",
                "is_featured": False,
            },
        ]

        # Delete existing homes to avoid duplicates
        AvailableHome.objects.all().delete()

        for i, home_data in enumerate(homes_data):
            home = AvailableHome.objects.create(
                title=home_data["title"],
                location=home_data["location"],
                price=home_data["price"],
                beds=home_data["beds"],
                baths=home_data["baths"],
                sqft=home_data["sqft"],
                status=home_data["status"],
                image_url=home_data["image_url"],
                is_featured=home_data["is_featured"],
                order=i,
            )
            self.stdout.write(f"Created home: {home.title}")

        self.stdout.write(self.style.SUCCESS("Successfully populated available homes data"))
