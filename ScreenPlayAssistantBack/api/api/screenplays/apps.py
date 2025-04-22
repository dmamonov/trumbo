"""Posts app"""

# Django
from django.apps import AppConfig


class ScreenPlayAppConfig(AppConfig):
    """ScreenPlay app config"""

    name = 'api.screenplays'
    verbose_name = 'Screen Plays'
    
    def ready(self):
        # Import and connect the signal
        from . import signals
