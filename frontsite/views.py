from django.shortcuts import render
from django.test import Client


def index(request):
    # Meta information
    meta = {
        "title": "CivicCore Engineering | Premium Consultancy",
        "description": "Engineering excellence from the ground up. We deliver innovative structural design, project management, and sustainable engineering solutions.",
    }

    # Hero section data
    hero = {
        "tagline": "Building Diaspora Dreams",
        "heading_main": "Find your Best",
        "heading_highlight": "Smart",
        "heading_suffix": "Real Estate.",
        "description": "TrustBuildUrban is a real estate solution that gives you the local scoop on homes in Kenya, backed by corporate transparency and elite design.",
        "cta_primary_text": "Get Started",
        "cta_secondary_text": "Watch video",
        "image_url": "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&q=80&w=1200",
        "verified_text": "Verified",
        "live_tracking_text": "Live Project Tracking",
        "company_name": "TrustBuild",
        "company_location": "Nairobi, Kenya",
        "stats": {
            "happy_customers": {"value": "5032", "label": "Happy Customers"},
            "property_sales": {"value": "6700+", "label": "Property Sales"},
            "award_winning": {"value": "205+", "label": "Award Winning"},
        },
    }

    # Statistics data
    stats_section = {
        "quote_text": "Integrity and innovation in every structure we touch. Engineering excellence from the ground up.",
        "landmark_projects": {"value": "850", "label_text": "Landmark Projects"},
        "client_reviews": {
            "rating": 5,
            "total_reviews": "12,000+",
            "label_text": "Client Reviews",
            "button_text": "Discover Excellence",
            "button_link": "#",
        },
    }

    # Diaspora challenge section
    diaspora_section = {
        "eyebrow": "The Diaspora Challenge",
        "heading": "Building in Kenya should not be a gamble.",
        "challenges": [
            {
                "title": "Fear of Misused Funds",
                "description": "Money sent for building being diverted for other family uses or personal gain.",
            },
            {
                "title": "Lack of Supervision",
                "description": "No one reliable to check site progress and quality on a daily basis.",
            },
            {
                "title": "Project Delays",
                "description": "Timelines stretching for years with no clear explanation or end date.",
            },
            {
                "title": "Poor Workmanship",
                "description": "Low-quality materials used despite paying premium prices.",
            },
            {
                "title": "Legal Risks",
                "description": "Issues with titles, county permits, and unlicensed contractors.",
            },
        ],
        "attribution": "TrustBuildUrban was founded to replace fear with structured, world-class building standards.",
        "featured_project": {
            "label": "Featured Project",
            "title": "The Grand Residence, Runda",
            "image_url": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?q=80&w=870&auto=format&fit=crop",
        },
    }

    feature_icon_width = 24
    feature_icon_height = 24

    # Features section
    features_section = {
        "eyebrow": "The TrustBuildUrban Standard",
        "heading": "Why Hundreds of Diaspora Families Trust Us",
        "features": [
            {
                "title": "Transparent Cost Breakdowns",
                "description": "Detailed bill of quantities before a single stone is moved.",
                "icon_path": """
                <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-file-text-icon lucide-file-text"><path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"/><path d="M14 2v5a1 1 0 0 0 1 1h5"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/></svg>
                """,
            },
            {
                "title": "Stage-Based Payments",
                "description": "Pay only for completed and verified construction milestones.",
                "icon_path": """ <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-calendar-check-icon lucide-calendar-check"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/><path d="m9 16 2 2 4-4"/></svg>
                """,
            },
            {
                "title": "Weekly Photo & Video Updates",
                "description": "Regular high-definition visual reporting of your site progress.",
                "icon_path": f"""
                    <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-eye-icon lucide-eye"><path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"/><circle cx="12" cy="12" r="3"/></svg>


                      """,
            },
            {
                "title": "Virtual Site Walkthroughs",
                "description": "Live video tours allowing you to inspect every corner remotely.",
                "icon_path": """
                <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-shield-check-icon lucide-shield-check"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/></svg>
                
                """,
            },
            {
                "title": "Legally Documented Contracts",
                "description": "Every project is backed by enforceable stamped legal agreements.",
                "icon_path": """,
                   <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-file-badge-icon lucide-file-badge"><path d="M13 22h5a2 2 0 0 0 2-2V8a2.4 2.4 0 0 0-.706-1.706l-3.588-3.588A2.4 2.4 0 0 0 14 2H6a2 2 0 0 0-2 2v3.3"/><path d="M14 2v5a1 1 0 0 0 1 1h5"/><path d="m7.69 16.479 1.29 4.88a.5.5 0 0 1-.698.591l-1.843-.849a1 1 0 0 0-.879.001l-1.846.85a.5.5 0 0 1-.692-.593l1.29-4.88"/><circle cx="6" cy="14" r="3"/></svg>
                """,
            },
            {
                "title": "Quality Assurance Team",
                "description": "Independent engineers verifying work against Kenyan building codes.",
                "icon_path": """
               <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-badge-check-icon lucide-badge-check"><path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"/><path d="m9 12 2 2 4-4"/></svg>
                """,
            },
        ],
    }

    # Steps section
    steps_section = {
        "eyebrow": "Transparent Execution",
        "heading": "Our 7-Step Architectural Journey",
        "description": "A meticulously structured process from initial concept to the day we hand over your keys.",
        "steps": [
        {
            "title": "Virtual Consultation",
            "description": "Define goals vision via high-level Zoom/Meet session.",
        },
        {
            "title": "Budget Planning",
            "description": "Detailed cost estimation and financial structuring.",
        },
        {
            "title": "Land Verification",
            "description": "Legal search and site analysis for clean title.",
        },
        {
            "title": "Architectural Design",
            "description": "Collaborative drafting of blueprints and 3D visuals.",
        },
        {
            "title": "Approvals & Documentation",
            "description": "Handling all NCA and County government permits.",
        },
        {
            "title": "Structured Construction",
            "description": "Phased build with weekly milestones and reports.",
        },
        {
            "title": "Handover & Warranty",
            "description": "Final inspection key handover and support.",
        },
    ]
    }

    # Services section
    services_section = {
        "subtitle": "Our Specializations",
        "heading": "Elite Engineering & Architectural Excellence",
        "services": [
            { "icon": """
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
            class="lucide w-10 h-10" aria-hidden="true">
            <path d="m2 22 1-1h3l9-9"></path><path d="M14 2h.01"></path><path d="M7 2h.01"></path><path d="M3.5 15.5 8 11"></path><path d="m5 11 3 3"></path><path d="M19 13.5v7a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2h7"></path><path d="M11 2h.01"></path><path d="m17 2 3.3 3.3c.39.39.39 1.02 0 1.41L17 10"></path><path d="M13 2v8"></path>
          </svg>
                """,
                "title": "Innovative Civil Engineering",
                "description": "Our engineering team focuses on structural integrity and future-proof solutions. We use advanced BIM modeling to ensure every beam and column is optimized for safety and efficiency.",
                "expertise": [
                    "Structural Analysis",
                    "Foundation Design",
                    "Retaining Walls",
                    "Drainage Systems",
                ],
            },
            {
                "icon": """
                 <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
            class="lucide w-10 h-10" aria-hidden="true">
            <path d="M3 14h18"></path><path d="M3 18h18"></path><path d="M4 10V4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v6"></path><path d="m12 2 4 4-4 4-4-4 4-4z"></path>
          </svg>
                """,
                "title": "Architectural Masterpieces",
            "description": "We believe architecture should tell a story. From ultra-modern villas to sustainable commercial hubs, our designs balance aesthetics with functionality and cultural context.",
            "expertise": [
                "Conceptual Design",
                "Interior Architecture",
                "Landscape Architecture",
                "Sustainable Architecture",
            ],
        },
    ]
    }

    # Portfolio section
    portfolio_section = {
        "heading": "Portfolio Highlights",
        "description": "Luxury and family homes delivered across the country.",
        "view_all_text": "View All Projects",
        # Fallback properties when no available_properties in context
        "fallback_properties": [
            {
                "title": "The Azure Villa",
                "location": "Runda, Nairobi",
                "type": "Luxury",
                "duration": "14 Months",
                "image_url": "https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&q=80&w=800",
            },
            {
                "title": "Oasis Heights",
                "location": "Karen, Nairobi",
                "type": "Villa",
                "duration": "12 Months",
                "image_url": "https://images.unsplash.com/photo-1616012760010-8da02da071fd?q=80&w=1032",
            },
            {
                "title": "Serene Ridge Estate",
                "location": "Tatu City, Kiambu",
                "type": "Family Home",
                "duration": "10 Months",
                "image_url": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&q=80&w=800",
            },
        ],
    }

    # Newsletter section
    newsletter = {
        "heading": "Free Diaspora Home Building Guide",
        "description": "Download our comprehensive manual on navigating land laws, approvals, and construction costs in Kenya from abroad.",
        "cta_text": "GET THE GUIDE",
        "placeholder": "Enter your email",
    }

    # Challenges data

    context = {
        # Meta
        "meta": meta,
        # Hero
        "hero": hero,
        # Stats
        "stats_section": stats_section,
        # Section titles
        "diaspora_section": diaspora_section,
        "features_section": features_section,
        "steps_section": steps_section,
        "services_section": services_section,
        "portfolio_section": portfolio_section,
        # Newsletter
        "newsletter": newsletter,
        "star_range": list(range(1, 6)),
    }

    return render(request, "homepage/index.html", context)


def about(request):
    """Render the about page"""
    # Meta information
    meta = {
        "title": "About | TrustBuild Urban",
        "description": "Learn about our mission of radical transparency and excellence in construction.",
    }

    # Story section data (hero section)
    story_section = {
        "eyebrow": "Our Story",
        "heading": "Excellence in Construction, Built on Trust.",
        "description_1": "Founded on the principle of radical transparency, TrustBuild Urban has become the premier choice for Kenyans living abroad and local high-end homeowners. We recognized a massive gap in the market: the lack of corporate accountability in residential construction.",
        "description_2": "Our mission is to provide a seamless, stress-free building experience where quality is never compromised, and every shilling is accounted for. We don't just build houses; we build legacies.",
        "image_url": "https://images.unsplash.com/photo-1541914590372-e01d89758e5a?auto=format&fit=crop&q=80&w=1200",
        "image_alt": "Architecture Team",
        "quote": "Transparency isn't a buzzword; it's our core architecture.",
        "stats": {
            "years_experience": {
                "value": "10+",
                "label": "Years Experience",
            },
            "projects_completed": {
                "value": "150+",
                "label": "Projects Completed",
            },
        },
    }

    # Core Pillars section data
    pillars_section = {
        "eyebrow": "The TrustBuild Standards",
        "heading": "Our Core Pillars",
        "pillars": [
            {
                "title": "Uncompromising Quality",
                "description": "We source premium materials and employ master craftsmen to ensure every finish is world-class.",
                "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-award w-8 h-8" aria-hidden="true"><path d="m15.477 12.89 1.515 8.526a.5.5 0 0 1-.81.47l-3.58-2.687a1 1 0 0 0-1.197 0l-3.586 2.686a.5.5 0 0 1-.81-.469l1.514-8.526"></path><circle cx="12" cy="8" r="6"></circle></svg>""",
            },
            {
                "title": "Client Partnership",
                "description": "We act as your local eyes and ears, treating your investment with the same care as our own.",
                "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-users w-8 h-8" aria-hidden="true"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><path d="M16 3.128a4 4 0 0 1 0 7.744"></path><path d="M22 21v-2a4 4 0 0 0-3-3.87"></path><circle cx="9" cy="7" r="4"></circle></svg>""",
            },
            {
                "title": "Ethical Conduct",
                "description": "From legal land acquisition to labor management, we operate with absolute integrity.",
                "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-circle-check-big w-8 h-8" aria-hidden="true"><path d="M21.801 10A10 10 0 1 1 17 3.335"></path><path d="m9 11 3 3L22 4"></path></svg>""",
            },
        ],
    }

    context = {
        "meta": meta,
        "story_section": story_section,
        "pillars_section": pillars_section,
    }

    return render(request, "about/about.html", context)


def available_homes(request):
    page = {
        "herosection": {
            "title": "Available Homes For Sale",
            "description": "High-quality homes built by TrustBuildUrban for immediate purchase. Move-in ready residences in Kenya's most sought-after neighborhoods.",
        },
        "homes": [
            {
                "id": "a1",
                "title": "The Sapphire Residence",
                "location": "Sigona, Kiambu",
                "price": "KES 45,000,000",
                "beds": 4,
                "baths": 4,
                "sqft": 3200,
                "status": "Available",
                "imageUrl": "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&q=80&w=1200",
            },
            {
                "id": "a2",
                "title": "Veranda Suites",
                "location": "Migaa, Kiambu",
                "price": "KES 38,500,000",
                "beds": 3,
                "baths": 3,
                "sqft": 2800,
                "status": "Under Offer",
                "imageUrl": "https://images.unsplash.com/photo-1518780664697-55e3ad937233?auto=format&fit=crop&q=80&w=1200",
            },
        ],
        "cta_Section": {
            "title": "Didn't find what you're looking for?",
            "description": "We can design and build a bespoke home specifically for you on your preferred piece of land.",
            "buttonText": "LEARN ABOUT CUSTOM BUILD",
            "buttonLink": "/available/",
        },
    }

    return render(request, "available_homes/available.html", {"pagedata": page})


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


def guide(request):
    """Render the guides page"""
    # Meta information
    meta = {
        "title": "Diaspora Guide | TrustBuild Urban",
        "description": "The comprehensive blueprint for Kenyans living abroad to invest back home.",
    }

    # Guide hero section
    guide_hero = {
        "eyebrow": "Free Resource",
        "heading": "The Diaspora Building Blueprint 2024",
        "description": "Our comprehensive 40-page guide for Kenyans living abroad who want to invest in high-end real estate and custom home construction back home.",
        "features": [
            "Navigating Kenya's land laws and title verification.",
            "Current construction costs per square meter (Luxury vs. Mid-Market).",
            "How to legally supervise your project from thousands of miles away.",
            "Managing family expectations vs. professional project management.",
            "The legal requirements for NCA and County approvals.",
        ],
        "image_url": "https://images.unsplash.com/photo-1586769852836-bc069f19e1b6?auto=format&fit=crop&q=80&w=800",
        "image_alt": "Guide Preview",
        "form": {
            "title": "Enter your details to receive the PDF",
            "name_placeholder": "Full Name",
            "email_placeholder": "Email Address",
            "button_text": "DOWNLOAD NOW",
        },
        "social_proof": {
            "avatars": [
                "https://i.pravatar.cc/100?u=1",
                "https://i.pravatar.cc/100?u=2",
                "https://i.pravatar.cc/100?u=3",
                "https://i.pravatar.cc/100?u=4",
            ],
            "text": "Join 2,400+ Diaspora Investors",
            "verified_text": "Verified by AAK Architects",
        },
    }

    context = {
        "meta": meta,
        "guide_hero": guide_hero,
    }

    return render(request, "guides/guide.html", context)


def process(request):
    """Render the process page"""
    # Meta information
    meta = {
        "title": "Our Process | TrustBuild Urban",
        "description": "Discover our 7-step roadmap to predictable construction results in Kenya.",
    }

    # Process header section
    process_header = {
        "eyebrow": "How We Work",
        "heading": "The 7-Step TrustBuild Roadmap",
        "description": "Construction in Kenya doesn't have to be chaotic. We use a standardized corporate workflow to ensure predictable results every time.",
    }

    # Process steps section
    process_steps = {
        "quality_gate_label": "Quality Gate",
        "quality_gate_text": "This stage must be signed off by both our lead engineer and the client before proceeding.",
        "steps": [
            {
                "title": "Consultation",
                "description": "Brainstorming and roadmap development.",
            },
            {
                "title": "Feasibility",
                "description": "Site visits and legal title verification.",
            },
            {
                "title": "Concept",
                "description": "Architectural designs and floor planning.",
            },
            {
                "title": "Approvals",
                "description": "NCA and County government legal sign-offs.",
            },
            {
                "title": "Contracts",
                "description": "Bill of quantities and fixed-price agreements.",
            },
            {
                "title": "Construction",
                "description": "Structured building with live video updates.",
            },
            {
                "title": "Handover",
                "description": "Quality verification and key ceremony.",
            },
        ],
    }

    # Process CTA section
    process_cta = {
        "heading": "Ready to take step one?",
        "button_text": "Book Initial Consultation",
    }

    context = {
        "meta": meta,
        "process_header": process_header,
        "process_steps": process_steps,
        "process_cta": process_cta,
    }

    return render(request, "process/process.html", context)


def services(request):
    """Render the services page"""
    # Meta information
    meta = {
        "title": "Our Services | TrustBuild Urban",
        "description": "Specialized solutions in construction, project management, and structural engineering by TrustBuild Urban.",
    }

    # Services header section
    services_header = {
        "eyebrow": "What We Do",
        "heading": "Specialized Solutions for Discerning Clients.",
        "description": "From the first site visit to the final coat of paint, we manage the complexities of construction so you don't have to.",
    }

    # Services list section
    services_list = {
        "learn_more_text": "Learn More",
        "services": [
            {
                "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-globe w-10 h-10" aria-hidden="true"><circle cx="12" cy="12" r="10"></circle><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"></path><path d="M2 12h20"></path></svg>""",
                "title": "Consultancy",
                "description": "Expert advice for your building project. We handle all the heavy lifting, ensuring your project meets both local regulations and international standards.",
                "image_url": "https://images.unsplash.com/photo-1541914590372-e01d89758e5a?auto=format&fit=crop&q=80&w=1200",
            },
            {
                "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-house w-10 h-10" aria-hidden="true"><path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"></path><path d="M3 10a2 2 0 0 1 .709-1.528l7-6a2 2 0 0 1 2.582 0l7 6A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path></svg>""",
                "title": "Construction",
                "description": "Quality builds you can trust. We manage master craftsmen and premium materials to ensure your legacy is built to the highest possible standards.",
                "image_url": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&q=80&w=1200",
            },
            {
                "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-settings w-10 h-10" aria-hidden="true"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"></path><circle cx="12" cy="12" r="3"></circle></svg>""",
                "title": "Project Management",
                "description": "We manage everything for you. From procurement to labor management, we act as your local eyes and ears, treating your investment with the same care as our own.",
                "image_url": "https://images.unsplash.com/photo-1541888946425-d81bb19480c5?auto=format&fit=crop&q=80&w=1200",
            },
            {
                "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-search w-10 h-10" aria-hidden="true"><circle cx="11" cy="11" r="8"></circle><path d="m21 21-4.3-4.3"></path></svg>""",
                "title": "Site Inspection",
                "description": "Regular checks on your progress. We provide detailed reports and live video updates, ensuring radical transparency throughout the building lifecycle.",
                "image_url": "https://images.unsplash.com/photo-1531834685032-c34bf0d84c77?auto=format&fit=crop&q=80&w=1200",
            },
        ],
    }

    context = {
        "meta": meta,
        "services_header": services_header,
        "services_list": services_list,
    }

    return render(request, "services/services.html", context)


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


def contact(request):
    """Render the contact page"""
    # Meta information
    meta = {
        "title": "Contact Us | TrustBuild Urban",
        "description": "Get in touch with TrustBuild Urban for your premium construction and design projects in Kenya.",
    }

    # Contact header section
    contact_header = {
        "eyebrow": "Get In Touch",
        "heading": "Let's Build Your Legacy Together.",
        "description": "Whether you're in the diaspora or local, we're here to provide the radical transparency and excellence your project deserves.",
    }

    # Contact content section
    contact_content = {
        "form": {
            "name_label": "Full Name",
            "name_placeholder": "John Doe",
            "email_label": "Email Address",
            "email_placeholder": "john@example.com",
            "subject_label": "Subject",
            "subject_options": [
                "New Project Inquiry",
                "Diaspora Consultation",
                "Partnership Proposal",
                "Other",
            ],
            "message_label": "Your Message",
            "message_placeholder": "Tell us about your project...",
            "submit_text": "Send Message",
        },
        "info": {
            "title": "Contact Information",
            "items": [
                {
                    "label": "Call Us",
                    "value": "+254 712 345 678",
                    "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-phone w-5 h-5"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>""",
                },
                {
                    "label": "Email Us",
                    "value": "info@trustbuildurban.co.ke",
                    "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-mail w-5 h-5"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7"/></svg>""",
                },
                {
                    "label": "Visit Us",
                    "value": "Riverside Square, Riverside Dr,<br>Nairobi, Kenya",
                    "icon": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-map-pin w-5 h-5"><path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/></svg>""",
                },
            ],
            "map": {
                "image_url": "https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?auto=format&fit=crop&q=80&w=1200",
                "alt_text": "Office Location Map",
                "label": "Office Location",
            },
        },
    }

    context = {
        "meta": meta,
        "contact_header": contact_header,
        "contact_content": contact_content,
    }

    return render(request, "contact/contact.html", context)
