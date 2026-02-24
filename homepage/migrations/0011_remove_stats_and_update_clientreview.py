# Generated manually to remove Stats/StatsSection and update ClientReview

from django.db import migrations, models
import django.db.models.deletion


def migrate_clientreview_to_homepage(apps, schema_editor):
    """
    Migrate ClientReview from StatsSection foreign key to HomePage foreign key.
    """
    ClientReview = apps.get_model('homepage', 'ClientReview')
    StatsSection = apps.get_model('homepage', 'StatsSection')
    
    for client_review in ClientReview.objects.all():
        # Get the related StatsSection to find the homepage
        try:
            stats_section = StatsSection.objects.get(client_reviews=client_review)
            client_review.homepage = stats_section.homepage
            client_review.save()
        except StatsSection.DoesNotExist:
            # If no StatsSection, try to get any homepage
            from homepage.models import HomePage
            homepage = HomePage.objects.first()
            if homepage:
                client_review.homepage = homepage
                client_review.save()


def reverse_migration(apps, schema_editor):
    """
    Reverse the migration - this will need manual cleanup of StatsSection.
    """
    pass  # This is a one-way migration to remove Stats/StatsSection


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0010_alter_clientreview_uuid_alter_diasporachallenge_uuid_and_more'),
    ]

    operations = [
        # Step 1: Add homepage field (nullable first)
        migrations.AddField(
            model_name='clientreview',
            name='homepage',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='client_reviews',
                to='homepage.homepage'
            ),
        ),
        
        # Step 2: Migrate data
        migrations.RunPython(
            migrate_clientreview_to_homepage,
            reverse_migration
        ),
        
        # Step 3: Make homepage non-nullable (if data was migrated)
        migrations.AlterField(
            model_name='clientreview',
            name='homepage',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='client_reviews',
                to='homepage.homepage'
            ),
        ),
        
        # Step 4: Remove stats_section field
        migrations.RemoveField(
            model_name='clientreview',
            name='stats_section',
        ),
        
        # Step 5: Delete Stats model
        migrations.DeleteModel(
            name='Stats',
        ),
        
        # Step 6: Delete StatsSection model
        migrations.DeleteModel(
            name='StatsSection',
        ),
    ]
