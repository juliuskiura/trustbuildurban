from django.shortcuts import render

def index(request):
    return render(request, 'homepage/index.html')


def available_homes(request):
    page = {
    "herosection": {
        "title": "Available Homes For Sale",
        "description": "High-quality homes built by Krestwood for immediate purchase. Move-in ready residences in Kenya's most sought-after neighborhoods.",
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