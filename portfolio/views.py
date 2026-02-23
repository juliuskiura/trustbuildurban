from django.shortcuts import render
from django.db.models import Prefetch

from .models import (
    PortfolioPage,
    PortfolioHeader,
    PortfolioProjectsSection,
    PortfolioProjectCategory,
    PortfolioProject,
    ProjectImage,
)


def portfolio(request):
    """Render the portfolio page"""
    # Get the published PortfolioPage
    portfolio_page = PortfolioPage.objects.filter(is_published=True).first()

    if not portfolio_page:
        # Fallback to any portfolio page
        portfolio_page = PortfolioPage.objects.first()

    # Meta information from page
    meta = {
        "title": (
            portfolio_page.meta_title
            if portfolio_page
            else "Our Portfolio | TrustBuild Urban"
        ),
        "description": (
            portfolio_page.meta_description
            if portfolio_page
            else "Explore our architectural masterpieces across Nairobi and Kiambu."
        ),
    }

    # Portfolio header section
    portfolio_header = None
    if portfolio_page:
        header = getattr(portfolio_page, "header_section", None)
        if header:
            portfolio_header = {
                "heading": header.heading,
                "description": header.description,
            }

    # Portfolio projects section
    portfolio_projects = None
    if portfolio_page:
        projects_section = portfolio_page.projects_sections.prefetch_related(
            Prefetch(
                "categories",
                queryset=PortfolioProjectCategory.objects.order_by("order"),
            ),
            Prefetch(
                "projects",
                queryset=PortfolioProject.objects.order_by("order").prefetch_related(
                    Prefetch(
                        "images", queryset=ProjectImage.objects.filter(is_cover=True)
                    )
                ),
            ),
        ).first()

        if projects_section:
            # Get filters
            filters = [cat.name for cat in projects_section.categories.all()]

            # Get projects
            projects = []
            for project in projects_section.projects.all():
                # Get cover image
                image_url = None
                cover_image = project.images.filter(is_cover=True).first()
                if cover_image:
                    image_url = cover_image.image_url or (
                        cover_image.image.image_url if cover_image.image else None
                    )

                projects.append(
                    {
                        "title": project.title,
                        "location": project.location,
                        "status": project.status,
                        "description": project.description,
                        "image_url": image_url,
                    }
                )

            portfolio_projects = {
                "filters": filters,
                "projects": projects,
            }

    context = {
        "meta": meta,
        "portfolio_header": portfolio_header,
        "portfolio_projects": portfolio_projects,
    }

    return render(request, "portfolio/portfolio.html", context)
