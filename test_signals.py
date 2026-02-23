#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tbusite.settings')
django.setup()

from images.models import Image, ImageUsage
from homepage.models import HeroSection
from django.contrib.contenttypes.models import ContentType

# Check current state
print('=== Current ImageUsage count ===')
print(f'Total ImageUsage records: {ImageUsage.objects.count()}')

print('\n=== HeroSections with background_image ===')
heroes = HeroSection.objects.exclude(background_image__isnull=True).exclude(background_image=None)
print(f'HeroSections with images: {heroes.count()}')
for hero in heroes:
    print(f'  - {hero} -> image: {hero.background_image}')

print('\n=== ContentTypes ===')
ct = ContentType.objects.get_for_model(HeroSection)
print(f'HeroSection content_type: {ct}')

print('\n=== Trying to get ImageUsage for HeroSection ===')
usages = ImageUsage.objects.filter(content_type=ct)
print(f'ImageUsage for HeroSection: {usages.count()}')

# Now test: save a HeroSection and see if ImageUsage gets created
print('\n=== Testing signal by re-saving HeroSection ===')
if heroes.exists():
    hero = heroes.first()
    print(f'Re-saving: {hero}')
    hero.save()
    
    # Check again
    usages_after = ImageUsage.objects.filter(content_type=ct)
    print(f'ImageUsage for HeroSection after save: {usages_after.count()}')
else:
    print('No HeroSections with images to test')
