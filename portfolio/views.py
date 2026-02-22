from django.shortcuts import render


def portfolio(request):
    """Render the portfolio page"""
    # Meta information
    meta = {
        "title": "Our Portfolio | TrustBuild Urban",
        "description": "Explore our architectural masterpieces across Nairobi and Kiambu.",
    }

    # Portfolio header section
    portfolio_header = {
        "heading": "Our Portfolio",
        "description": "A showcase of architectural brilliance and construction precision across Nairobi, Kiambu, and beyond.",
    }

    # Portfolio projects section
    portfolio_projects = {
        "filters": ["All", "Ongoing", "Luxury", "Family Home", "Villa", "Mid-Market"],
        "projects": [
            {
                "title": "Mountain View Estate",
                "location": "Kiambu Road, Kiambu",
                "status": "Ongoing",
                "description": "A premium gated community featuring modern architectural lines and sustainable materials.",
                "image_url": "/static/images/build1.jpeg",
            },
            {
                "title": "The Urban Retreat",
                "location": "Lavington, Nairobi",
                "status": "Ongoing",
                "description": "Sophisticated metropolitan living with an emphasis on privacy and luxury finishes.",
                "image_url": "/static/images/build2.jpeg",
            },
            {
                "title": "Azure Heights",
                "location": "Parklands, Nairobi",
                "status": "Ongoing",
                "description": "Contemporary luxury apartments with panoramic city views and world-class amenities.",
                "image_url": "/static/images/build3.jpeg",
            },
            {
                "title": "Sunset Ridge",
                "location": "Ngong, Kajiado",
                "status": "Ongoing",
                "description": "Family living redefined with expansive outdoor spaces and modern functional design.",
                "image_url": "/static/images/build4.jpeg",
            },
            {
                "title": "The Heritage Villa",
                "location": "Tigoni, Kiambu",
                "status": "Ongoing",
                "description": "A timeless blend of classical architectural elements and contemporary luxury.",
                "image_url": "/static/images/build5.jpeg",
            },
            {
                "title": "Savanna Heights",
                "location": "Runda, Nairobi",
                "status": "Ongoing",
                "description": "Exclusive villa development with seamless indoor-outdoor living spaces.",
                "image_url": "/static/images/build6.jpeg",
            },
        ],
    }

    context = {
        "meta": meta,
        "portfolio_header": portfolio_header,
        "portfolio_projects": portfolio_projects,
    }

    return render(request, "portfolio/portfolio.html", context)
