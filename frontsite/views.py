from django.shortcuts import render

def index(request):
    # Data for the homepage redesign
    challenges = [
        "Fear of Misused Funds",
        "Lack of Supervision",
        "Project Delays",
        "Poor Workmanship",
        "Legal Risks"
    ]
    
    features = [
        {
            "title": "Transparent Cost Breakdowns",
            "description": "Detailed bill of quantities before a single stone is moved.",
            "icon_path": "M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z,M14 2v5a1 1 0 0 0 1 1h5,M10 9H8,M16 13H8,M16 17H8"
        },
        {
            "title": "Stage-Based Payments",
            "description": "Pay only for completed and verified construction milestones.",
            "icon_path": "M8 2v4,M16 2v4,rect width=\"18\" height=\"18\" x=\"3\" y=\"4\" rx=\"2\",M3 10h18"
        },
        {
            "title": "Weekly Photo & Video Updates",
            "description": "Regular high-definition visual reporting of your site progress.",
            "icon_path": "M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0,circle cx=\"12\" cy=\"12\" r=\"3\""
        },
        {
            "title": "Virtual Site Walkthroughs",
            "description": "Live video tours allowing you to inspect every corner remotely.",
            "icon_path": "M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z,m9 12 2 2 4-4"
        },
        {
            "title": "Legally Documented Contracts",
            "description": "Every project is backed by enforceable stamped legal agreements.",
            "icon_path": "M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z,m9 12 2 2 4-4"
        },
        {
            "title": "Quality Assurance Team",
            "description": "Independent engineers verifying work against Kenyan building codes.",
            "icon_path": "M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.106-3.105c.32-.322.863-.22.983.218a6 6 0 0 1-8.259 7.057l-7.91 7.91a1 1 0 0 1-2.999-3l7.91-7.91a6 6 0 0 1 7.057-8.259c.438.12.54.662.219.984z"
        }
    ]
    
    steps = [
        {"title": "Virtual Consultation", "description": "Define goals vision via high-level Zoom/Meet session."},
        {"title": "Budget Planning", "description": "Detailed cost estimation and financial structuring."},
        {"title": "Land Verification", "description": "Legal search and site analysis for clean title."},
        {"title": "Architectural Design", "description": "Collaborative drafting of blueprints and 3D visuals."},
        {"title": "Approvals & Documentation", "description": "Handling all NCA and County government permits."},
        {"title": "Structured Construction", "description": "Phased build with weekly milestones and reports."},
        {"title": "Handover & Warranty", "description": "Final inspection key handover and support."}
    ]
    
    expertise = [
        "Structural Design", "Project Supervision", "Feasibility Studies", "Topographical Surveys",
        "Concept Visualization", "Interior Design", "Landscape Planning", "Sustainable Design"
    ]
    
    context = {
        "challenges": challenges,
        "features": features,
        "steps": steps,
        "expertise": expertise,
        "star_range": list(range(1, 6))
    }
    
    return render(request, "homepage/index.html", context)


def available_homes(request):
    page = {
    "herosection": {
        "title": "Available Homes For Sale",
        "description": "High-quality homes built by TrustBuildUrban for immediate purchase. Move-in ready residences in Kenya's most sought-after neighborhoods.",
},
'homes':  [{
    'id': 'a1',
    'title': 'The Sapphire Residence',
    'location': 'Sigona, Kiambu',
    'price': 'KES 45,000,000',
    'beds': 4,
    'baths': 4,
    'sqft': 3200,
    'status': 'Available',
    'imageUrl': 'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&q=80&w=1200'
  },
  {
    'id': 'a2',
    'title': 'Veranda Suites',
    'location': 'Migaa, Kiambu',
    'price': 'KES 38,500,000',
    'beds': 3,
    'baths': 3,
    'sqft': 2800,
    'status': 'Under Offer',
    'imageUrl': 'https://images.unsplash.com/photo-1518780664697-55e3ad937233?auto=format&fit=crop&q=80&w=1200'
  }
  ],

'cta_Section': {
    'title': "Didn't find what you're looking for?",
    'description': "We can design and build a bespoke home specifically for you on your preferred piece of land.",
    'buttonText': 'LEARN ABOUT CUSTOM BUILD',
    'buttonLink': '/available/'}

}
    
    return render(request, 'available_homes/available.html', {'pagedata': page})
