"""Events app"""

# Django
from django.apps import AppConfig


class EventsAppConfig(AppConfig):
    """Events app config"""

    name = 'api.events'
    verbose_name = 'Events'
    
    def ready(self):
        from . import signals
