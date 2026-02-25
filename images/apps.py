from django.apps import AppConfig


class ImagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'images'
    verbose_name = 'Images'

    def ready(self):
        """
        Initialize the images app.
        Register all models that have ForeignKey to Image and connect signals.
        """
        # Import signals module to register signal handlers
        from images import signals

        # Register models that have ForeignKey to Image
        # Format: (model_class, field_name)

        # Blog models
        from blog.models import BlogPost

        signals.register_image_foreign_key(BlogPost, "image")

        # Portfolio models
        from portfolio.models import ProjectImage

        signals.register_image_foreign_key(ProjectImage, "image")

        # About models
        from about.models import HeroSection

        signals.register_image_foreign_key(HeroSection, "image")

        # Homepage models
        from homepage.models import HeroSection as HomeHeroSection

        signals.register_image_foreign_key(HomeHeroSection, "background_image")

        from homepage.models import DiasporaSection

        signals.register_image_foreign_key(DiasporaSection, "featured_image")

        # Services models
        from services.models import Service

        signals.register_image_foreign_key(Service, "image")

        # Available Homes models
        from available_homes.models import AvailableHome, AvailableHomeImage

        signals.register_image_foreign_key(AvailableHome, "image")
        signals.register_image_foreign_key(AvailableHomeImage, "image")

        # Connect the signals
        signals.connect_signals()
