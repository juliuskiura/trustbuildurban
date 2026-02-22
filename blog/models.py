from django.db import models
from pages.models import Page


class BlogPage(Page):
    """
    BlogPage model that inherits from the base Page model.
    This allows creating blog page content from the admin panel.
    """
    # Additional fields specific to blog page
    blog_eyebrow = models.CharField(max_length=100, blank=True)
    blog_heading = models.CharField(max_length=200, blank=True)
    blog_description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Blog Page'
        verbose_name_plural = 'Blog Pages'

    def get_template(self):
        return "blog/blog.html"

    def serve(self, request):
        from django.shortcuts import render
        from .views import blog
        return blog(request)
