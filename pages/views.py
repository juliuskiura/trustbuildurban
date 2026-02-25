from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils import timezone
from .models import Page


def page_detail(request, path=None):
    """
    Serve a page based on its path.
    Similar to Wagtail's page serving.
    """
    # If no path provided, try to get the homepage
    if not path:
        # Use the Page model's get_root_page method which handles inheritance properly
        page = Page.get_root_page()
        if page:
            return page.get_specific().serve(request)
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

        return page.get_specific().serve(request)

    except Page.DoesNotExist:
        raise Http404(f"Page not found: {path}")


def page_by_id(request, page_id):
    """Serve a page by its ID (fallback method)."""
    page = get_object_or_404(Page, pk=page_id, is_published=True)
    return page.get_specific().serve(request)


def preview_page(request, page_id):
    """Preview a page (even if not published)."""
    from django.contrib.auth.decorators import login_required
    
    page = get_object_or_404(Page, pk=page_id)
    
    # Check permissions
    if not request.user.has_perm('pages.change_page'):
        raise Http404("You don't have permission to preview this page")
    
    return page.get_specific().serve(request)


def get_menu_pages():
    """Helper function to get pages that should appear in menus."""
    return Page.objects.filter(
        is_published=True,
        show_in_menus=True
    ).order_by('tree_id', 'lft')
