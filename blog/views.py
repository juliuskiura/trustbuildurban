from django.shortcuts import render
from django.db.models import Prefetch

from .models import (
    BlogPage,
    BlogHeader,
    BlogGridSection,
    BlogPost,
)


def blog(request):
    """Render the blog page"""
    # Get the published BlogPage
    blog_page = BlogPage.objects.filter(is_published=True).first()

    if not blog_page:
        # Fallback to any blog page
        blog_page = BlogPage.objects.first()

    # Meta information from page
    meta = {
        "title": blog_page.meta_title if blog_page else "Blog | TrustBuild Urban",
        "description": (
            blog_page.meta_description
            if blog_page
            else "Stay updated with the latest in Kenyan construction, architectural trends, and diaspora investment strategies."
        ),
    }

    # Blog header section
    blog_header = None
    if blog_page:
        header = getattr(blog_page, "header_section", None)
        if header:
            blog_header = {
                "eyebrow": header.eyebrow,
                "heading": header.heading,
                "description": header.description,
            }

    # Blog grid section
    blog_grid = None
    if blog_page:
        blog_section = blog_page.blog_sections.prefetch_related(
            Prefetch("posts", queryset=BlogPost.objects.order_by("order")),
        ).first()

        if blog_section:
            # Get posts
            posts = []
            for post in blog_section.posts.all():
                # Get image URL
                image_url = post.image_url or (
                    post.image.image_url if post.image else None
                )

                posts.append(
                    {
                        "title": post.title,
                        "excerpt": post.excerpt,
                        "category": post.category,
                        "date": post.date,
                        "image_url": image_url,
                    }
                )

            blog_grid = {
                "read_more_text": blog_section.read_more_text,
                "posts": posts,
            }

    context = {
        "meta": meta,
        "blog_header": blog_header,
        "blog_grid": blog_grid,
    }

    return render(request, "blog/blog.html", context)
