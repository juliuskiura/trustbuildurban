from django.db import models
from pages.models import Page
from core.models import PageBase
from ordered_model.models import OrderedModel


class BlogPage(Page):
    """
    BlogPage model that inherits from the base Page model.
    This allows creating blog page content from the admin panel.
    """

    class Meta:
        verbose_name = 'Blog Page'
        verbose_name_plural = 'Blog Pages'

    def get_template(self):
        return "blog/blog.html"

    def serve(self, request):
        from django.shortcuts import render
        from .views import blog
        return blog(request)


class BlogHeader(PageBase):
    """
    Blog header section model with OneToOne relationship to BlogPage.
    Contains the eyebrow, heading, and description for the blog page.
    """

    blog_page = models.OneToOneField(
        "blog.BlogPage", on_delete=models.CASCADE, related_name="header_section"
    )

    # Header content
    eyebrow = models.CharField(max_length=100, blank=True, default="Building Trends")
    heading = models.CharField(
        max_length=200, blank=True, default="TrustBuild Insights"
    )
    description = models.TextField(
        blank=True,
        default="Stay updated with the latest in Kenyan construction, architectural trends, and diaspora investment strategies.",
    )

    class Meta:
        verbose_name = "Blog Header"
        verbose_name_plural = "Blog Headers"

    def __str__(self):
        return f"Blog Header for {self.blog_page.title}"


class BlogGridSection(PageBase):
    """
    Blog grid section model with ForeignKey to BlogPage.
    Contains read more text and blog posts.
    """

    blog_page = models.ForeignKey(
        "blog.BlogPage", on_delete=models.CASCADE, related_name="blog_sections"
    )

    # Section content
    read_more_text = models.CharField(max_length=100, blank=True, default="Read More")

    class Meta:
        verbose_name = "Blog Grid Section"
        verbose_name_plural = "Blog Grid Sections"

    def __str__(self):
        return f"Blog Grid for {self.blog_page.title}"


class BlogPost(PageBase, OrderedModel):
    """
    Blog post model for individual blog posts.
    Uses OrderedModel for ordering posts.
    """

    blog_section = models.ForeignKey(
        BlogGridSection, on_delete=models.CASCADE, related_name="posts"
    )

    # Post content
    title = models.CharField(max_length=200, blank=True)
    excerpt = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True, default="Construction")
    date = models.CharField(max_length=50, blank=True)

    # Image - using ForeignKey to Image model
    image = models.ForeignKey(
        "images.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_post_images",
    )
    image_url = models.URLField(max_length=500, blank=True, null=True)

    # Order
    order_with_respect_to = "blog_section"

    class Meta(OrderedModel.Meta):
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        return self.title
