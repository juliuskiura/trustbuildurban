from django.shortcuts import render


def blog(request):
    """Render the blog page"""
    # Meta information
    meta = {
        "title": "Blog | TrustBuild Urban",
        "description": "Stay updated with the latest in Kenyan construction, architectural trends, and diaspora investment strategies.",
    }

    # Blog header section
    blog_header = {
        "eyebrow": "Building Trends",
        "heading": "TrustBuild Insights",
        "description": "Stay updated with the latest in Kenyan construction, architectural trends, and diaspora investment strategies.",
    }

    # Blog grid section
    blog_grid = {
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

    context = {
        "meta": meta,
        "blog_header": blog_header,
        "blog_grid": blog_grid,
    }

    return render(request, "blog/blog.html", context)
