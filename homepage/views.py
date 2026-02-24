from django.shortcuts import render
from django.http import Http404
from .models import (
    Page,
    HomePage,
    NewsletterSection,
    PortFolioSection,
)
from portfolio.models import PortfolioProject


def index(request):
    # Get the homepage
    homepage = (
        HomePage.objects.select_related("hero_section")
        .prefetch_related(
            "hero_section__buttons",
            "client_reviews",
            "diaspora_sections",
            "diaspora_sections__challenges",
            "features_sections",
            "features_sections__features",
            "steps_sections",
            "steps_sections__steps",
            "services_sections",
            "services_sections__services",
            "newsletter_sections",
            "newsletter_sections__buttons",
            "who_we_are_section",
            "stats_section",
            "stats_section__stats",
            "portfolio_sections",
        )
        .filter(is_published=True)
        .first()
    )

    if not homepage:
        homepage = HomePage.objects.first()

    # Meta information
    meta = {}
    if homepage:
        meta = {
            "title": homepage.meta_title or "",
            "description": homepage.meta_description or "",
        }

    # Hero section data from model
    hero = {
        "tagline": "",
        "heading_main": "",
        "heading_highlight": "",
        "heading_suffix": "",
        "description": "",
        "buttons": [],
        "image_url": "",
        "verified_text": "",
        "live_tracking_text": "",
        "company_name": "",
        "company_location": "",
        "stats": {},
    }

    hero_section = getattr(homepage, "hero_section", None)
    if hero_section:
        # Get buttons (already prefetched)
        hero_buttons = []
        for button in hero_section.buttons.all():
            hero_buttons.append(
                {
                    "text": button.text,
                    "link": button.link,
                    "icon": button.icon,
                    "style": button.style,
                    "size": button.size,
                    "is_external": button.is_external,
                    "is_full_width": button.is_full_width,
                }
            )

        hero = {
            "tagline": hero_section.tagline,
            "heading_main": hero_section.heading_main,
            "heading_highlight": hero_section.heading_highlight,
            "heading_suffix": hero_section.heading_suffix,
            "description": hero_section.description,
            "buttons": hero_buttons,
            "image_url": (
                hero_section.background_image.image_url
                if hero_section.background_image
                else ""
            ),
            "verified_text": hero_section.verified_text,
            "live_tracking_text": hero_section.live_tracking_text,
            "company_name": hero_section.company_name,
            "company_location": hero_section.company_location,
            "show_verified_badge": hero_section.show_verified_badge,
            "show_live_tracking": hero_section.show_live_tracking,
        }

    # Client review data from model
    client_review_data = {
        "rating": 0,
        "total_reviews": "",
        "label_text": "",
        "button_text": "",
        "button_link": "",
    }

    client_review_obj = getattr(homepage, "client_reviews", None)
    if client_review_obj and client_review_obj.exists():
        client_review_obj = client_review_obj.first()
        client_review_data = {
            "rating": client_review_obj.rating,
            "total_reviews": client_review_obj.total_reviews,
            "label_text": client_review_obj.label_text,
            "button_text": client_review_obj.button_text,
            "button_link": client_review_obj.button_link,
        }

    # Diaspora section data from model
    diaspora_section_data = {
        "eyebrow": "",
        "heading": "",
        "challenges": [],
        "attribution": "",
        "featured_project": {
            "label": "",
            "title": "",
            "image_url": "",
        },
    }

    diaspora_section = getattr(homepage, "diaspora_sections", None)
    if diaspora_section and diaspora_section.exists():
        diaspora_section = diaspora_section.first()
        diaspora_section_data = {
            "eyebrow": diaspora_section.eyebrow,
            "heading": diaspora_section.heading,
            "attribution": diaspora_section.attribution,
            "challenges": [],
            "featured_project": {
                "label": diaspora_section.featured_label,
                "title": diaspora_section.featured_title,
                "image_url": (
                    diaspora_section.featured_image.image_url
                    if diaspora_section.featured_image
                    else diaspora_section.featured_image_url
                ),
            },
        }
        # Get challenges (already prefetched)
        for challenge in diaspora_section.challenges.all():
            diaspora_section_data["challenges"].append(
                {
                    "title": challenge.title,
                    "description": challenge.description,
                }
            )

    # Features section data from model
    features_section_data = {
        "eyebrow": "",
        "heading": "",
        "features": [],
    }

    features_section = getattr(homepage, "features_sections", None)
    if features_section and features_section.exists():
        features_section = features_section.first()
        features_section_data = {
            "eyebrow": features_section.eyebrow,
            "heading": features_section.heading,
            "features": [],
        }
        # Get features (already prefetched)
        for feature in features_section.features.all():
            features_section_data["features"].append(
                {
                    "title": feature.title,
                    "description": feature.description,
                    "icon_path": feature.icon_path,
                }
            )

    # Steps section data from model
    steps_section_data = {
        "eyebrow": "",
        "heading": "",
        "description": "",
        "steps": [],
    }

    steps_section = getattr(homepage, "steps_sections", None)
    if steps_section and steps_section.exists():
        steps_section = steps_section.first()
        steps_section_data = {
            "eyebrow": steps_section.eyebrow,
            "heading": steps_section.heading,
            "description": steps_section.description,
            "steps": [],
        }
        # Get steps (already prefetched)
        for step in steps_section.steps.all():
            steps_section_data["steps"].append(
                {
                    "title": step.title,
                    "description": step.description,
                }
            )

    # Services section data from model
    services_section_data = {
        "subtitle": "",
        "heading": "",
        "services": [],
    }

    services_section = getattr(homepage, "services_sections", None)
    if services_section and services_section.exists():
        services_section = services_section.first()
        services_section_data = {
            "subtitle": services_section.subtitle,
            "heading": services_section.heading,
            "services": [],
        }
        # Get services (already prefetched)
        for service in services_section.services.all():
            # Parse expertise from comma-separated string to list
            expertise_list = []
            if service.expertise:
                expertise_list = [e.strip() for e in service.expertise.split(",")]

            services_section_data["services"].append(
                {
                    "title": service.title,
                    "description": service.description,
                    "icon": service.icon,
                    "expertise": expertise_list,
                }
            )

    # Newsletter section data from model
    newsletter_data = {
        "heading": "",
        "description": "",
        "cta_text": "",
        "placeholder": "",
    }

    newsletter_section = getattr(homepage, "newsletter_sections", None)
    if newsletter_section and newsletter_section.exists():
        newsletter_section = newsletter_section.first()
        newsletter_data = {
            "heading": newsletter_section.heading,
            "description": newsletter_section.description,
            "placeholder": newsletter_section.placeholder,
            "cta_text": "GET THE GUIDE",
        }
        # Get CTA button if exists (already prefetched)
        cta_button = newsletter_section.buttons.first()
        if cta_button:
            newsletter_data["cta_text"] = cta_button.text

    # Who We Are section data from model
    who_we_are_data = {
        "label": "",
        "heading": "",
        "description": "",
        "button_text": "",
        "button_link": "",
        "background_image_url": "",
    }

    who_we_are_section = getattr(homepage, "who_we_are_section", None)
    if who_we_are_section:
        who_we_are_data = {
            "label": who_we_are_section.label,
            "heading": who_we_are_section.heading,
            "description": who_we_are_section.description,
            "button_text": who_we_are_section.button_text,
            "button_link": who_we_are_section.button_link,
            "background_image_url": (
                who_we_are_section.background_image.image_url
                if who_we_are_section.background_image
                else who_we_are_section.background_image_url
            ),
        }

    # Stats section data from model
    stats_section_data = {
        "header": "",
        "background_pattern": "",
        "stats": [],
    }

    stats_section = getattr(homepage, "stats_section", None)
    if stats_section:
        stats_data = []
        for stat in stats_section.stats.all():
            stats_data.append(
                {
                    "number": stat.number,
                    "subtitle": stat.subtitle,
                }
            )
        stats_section_data = {
            "header": stats_section.header,
            "background_pattern": (
                stats_section.background_pattern.image_url
                if stats_section.background_pattern
                else ""
            ),
            "stats": stats_data,
        }

    # Portfolio section data - fetch highlighted projects from portfolio app
    available_properties = []
    try:
        # Get highlighted projects from PortfolioProject
        highlighted_projects = PortfolioProject.objects.filter(highlight_project=True)[
            :3
        ]
       
    except Exception as e:
        print(f"Error fetching portfolio projects: {e}")
        pass

    # Get portfolio section from database
    portfolio_section = {
        "heading": "",
        "description": "",
        "view_all_text": "",
    }
    portfolio_sections = getattr(homepage, "portfolio_sections", None)
    if portfolio_sections and portfolio_sections.exists():
        portfolio_obj = portfolio_sections.first()
        portfolio_section = {
            "heading": portfolio_obj.heading,
            "description": portfolio_obj.description,
            "view_all_text": portfolio_obj.button_text,
        }

    context = {
        # Meta
        "meta": meta,
        # Hero
        "hero": hero,
        # Client Review
        "client_review": client_review_data,
        # Sections from models
        "diaspora_section": diaspora_section_data,
        "features_section": features_section_data,
        "steps_section": steps_section_data,
        "services_section": services_section_data,
        # Portfolio
        "portfolio_section": portfolio_section,
        "available_properties": highlighted_projects,
        # Newsletter
        "newsletter": newsletter_data,
        # New sections
        "who_we_are": who_we_are_data,
        "stats_section": stats_section_data,
        "star_range": list(range(1, 6)),
    }

    return render(request, "homepage/index.html", context)


def page_detail(request, path=None):
    """
    Serve a page based on its path from the database.
    Uses the Page model to render dynamic pages.
    """
    # If no path provided, use the Page model's get_root_page method
    if not path:
        from pages.models import Page

        page = Page.get_root_page()
        if page:
            return page.serve(request)
        raise Http404("No root page found")

    # Split the path into segments
    path_segments = path.strip('/').split('/')

    # Try to find the page by slug chain
    try:
        # Get all pages at the root level matching the first segment
        page = Page.objects.get(slug=path_segments[0], parent__isnull=True, is_published=True)

        # Navigate down the tree
        for segment in path_segments[1:]:
            page = Page.objects.get(slug=segment, parent=page, is_published=True)

        return page.serve(request)

    except Page.DoesNotExist:
        raise Http404(f"Page not found: {path}")


def page_by_id(request, page_id):
    """Serve a page by its ID (fallback method)."""
    from django.shortcuts import get_object_or_404
    page = get_object_or_404(Page, pk=page_id, is_published=True)
    return page.serve(request)


def preview_page(request, page_id):
    """Preview a page (even if not published)."""
    from django.shortcuts import get_object_or_404
    from django.contrib.auth.decorators import login_required
    
    page = get_object_or_404(Page, pk=page_id)
    
    # Check permissions
    if not request.user.has_perm('homepage.change_page'):
        raise Http404("You don't have permission to preview this page")
    
    return page.serve(request)
