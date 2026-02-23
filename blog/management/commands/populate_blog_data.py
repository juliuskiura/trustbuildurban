"""
Management command to populate blog page sections data from views.py into the database models.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from blog.models import (
    BlogPage,
    BlogHeader,
    BlogGridSection,
    BlogPost,
)


class Command(BaseCommand):
    help = "Populate blog page sections with data from views.py"

    def add_arguments(self, parser):
        parser.add_argument(
            "--blog-id",
            type=int,
            help="ID of the BlogPage to populate data for. If not provided, will use the first published BlogPage.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be created without making changes.",
        )

    def handle(self, *args, **options):
        blog_id = options.get("blog_id")
        dry_run = options.get("dry_run", False)

        # Get the BlogPage or create one if it doesn't exist
        if blog_id:
            try:
                blog_page = BlogPage.objects.get(pk=blog_id)
            except BlogPage.DoesNotExist:
                self.stderr.write(
                    self.style.ERROR(f"BlogPage with ID {blog_id} does not exist.")
                )
                return
        else:
            blog_page = BlogPage.objects.filter(is_published=True).first()
            if not blog_page:
                # Try to get any blog page
                blog_page = BlogPage.objects.first()
                if not blog_page:
                    # Create a default BlogPage
                    self.stdout.write(self.style.WARNING("No BlogPage found. Creating a default BlogPage..."))
                    blog_page = BlogPage.objects.create(
                        title="Blog",
                        slug="blog",
                        is_published=True,
                        meta_title="Blog | TrustBuild Urban",
                        meta_description="Stay updated with the latest in Kenyan construction, architectural trends, and diaspora investment strategies."
                    )
                    self.stdout.write(self.style.SUCCESS(f"Created BlogPage: {blog_page.title} (ID: {blog_page.pk})"))

        self.stdout.write(self.style.SUCCESS(f"Using BlogPage: {blog_page.title} (ID: {blog_page.pk})"))

        if dry_run:
            self._print_dry_run(blog_page)
            return

        # Data from views.py
        blog_header_data = {
            "eyebrow": "Building Trends",
            "heading": "TrustBuild Insights",
            "description": "Stay updated with the latest in Kenyan construction, architectural trends, and diaspora investment strategies.",
        }

        blog_grid_data = {
            "read_more_text": "Read More",
            "posts": [
                {
                    "category": "Construction",
                    "date": "Oct 24, 2024",
                    "title": "Coming Soon: Building Your Legacy",
                    "excerpt": "We are preparing a series of deep dives into the Kenyan building landscape. Stay tuned for expert insights.",
                    "image_url": None,
                },
                {
                    "category": "Construction",
                    "date": "Oct 24, 2024",
                    "title": "Coming Soon: Building Your Legacy",
                    "excerpt": "We are preparing a series of deep dives into the Kenyan building landscape. Stay tuned for expert insights.",
                    "image_url": None,
                },
                {
                    "category": "Construction",
                    "date": "Oct 24, 2024",
                    "title": "Coming Soon: Building Your Legacy",
                    "excerpt": "We are preparing a series of deep dives into the Kenyan building landscape. Stay tuned for expert insights.",
                    "image_url": None,
                },
            ],
        }

        # Create the sections
        with transaction.atomic():
            # 1. Create or Update Blog Header
            header, created = BlogHeader.objects.update_or_create(
                blog_page=blog_page,
                defaults={
                    "eyebrow": blog_header_data["eyebrow"],
                    "heading": blog_header_data["heading"],
                    "description": blog_header_data["description"],
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} BlogHeader (ID: {header.pk})"
                )
            )

            # 2. Create or Update Blog Grid Section
            blog_section, created = BlogGridSection.objects.update_or_create(
                blog_page=blog_page,
                defaults={
                    "read_more_text": blog_grid_data["read_more_text"],
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} BlogGridSection (ID: {blog_section.pk})"
                )
            )

            # Create Blog Posts
            for idx, post_data in enumerate(blog_grid_data["posts"]):
                post, created = BlogPost.objects.update_or_create(
                    blog_section=blog_section,
                    title=post_data["title"],
                    defaults={
                        "excerpt": post_data["excerpt"],
                        "category": post_data["category"],
                        "date": post_data["date"],
                        "image_url": post_data.get("image_url"),
                        "order": idx + 1,
                    },
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  {'Created' if created else 'Updated'} Blog Post: {post.title}"
                    )
                )

        self.stdout.write(self.style.SUCCESS("\n=== Data population complete! ==="))

    def _print_dry_run(self, blog_page):
        """Print what would be created in dry run mode."""
        self.stdout.write(f"BlogPage: {blog_page.title} (ID: {blog_page.pk})\n")

        self.stdout.write("1. BlogHeader:")
        self.stdout.write(f"   - eyebrow: Building Trends")
        self.stdout.write(f"   - heading: TrustBuild Insights")

        self.stdout.write("\n2. BlogGridSection:")
        self.stdout.write(f"   - read_more_text: Read More")
        self.stdout.write("   - Blog Posts:")
        self.stdout.write("     * Coming Soon: Building Your Legacy (3 times)")
