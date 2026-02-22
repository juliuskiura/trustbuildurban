from django.db import models
from pages.models import Page


class PortfolioPage(Page):
    """
    PortfolioPage model that inherits from the base Page model.
    This allows creating portfolio page content from the admin panel.
    """
    # Additional fields specific to portfolio page
    portfolio_heading = models.CharField(max_length=200, blank=True)
    portfolio_description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Portfolio Page'
        verbose_name_plural = 'Portfolio Pages'

    def get_template(self):
        return "portfolio/portfolio.html"

    def serve(self, request):
        from django.shortcuts import render
        from .views import portfolio
        return portfolio(request)
