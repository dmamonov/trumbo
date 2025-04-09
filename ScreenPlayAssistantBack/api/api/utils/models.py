""" Django models utilities """

from django.conf import settings
# Django
from django.db import models
# Utils
from pytz import timezone as pztimezone


class BaseModel(models.Model):
    """ Base model

    Act as an abstract model and all the models in the project should will inherit from it.
    """

    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Date time on which the object was created.'
    )

    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text='Date time on which the object was modified.'
    )

    deleted = models.BooleanField(
        default=False,
        help_text='Set to False when an element is deleted'
    )

    class Meta:
        abstract = True
        get_latest_by = 'created'
        ordering = ['-created', '-modified']

    @property
    def proper_created(self):
        settings_time_zone = pztimezone(settings.TIME_ZONE)
        return self.created.astimezone(settings_time_zone).strftime('%d %B, %Y %I:%M %p')

    @property
    def proper_modified(self):
        settings_time_zone = pztimezone(settings.TIME_ZONE)
        return self.modified.astimezone(settings_time_zone).strftime('%d %B, %Y %I:%M %p')

    @property
    def is_modified(self):
        if self.modified.strftime('%d %B, %Y %I:%M %p') == self.created.strftime('%d %B, %Y %I:%M %p'):
            return None
        settings_time_zone = pztimezone(settings.TIME_ZONE)
        return self.modified.astimezone(settings_time_zone).strftime('%d %B, %Y %I:%M %p')

    def get_owner(self):
        pass

    def can_modify(self, user, *args, **kwargs):
        return self.get_owner() == user or user.is_app_superuser()

    def raw_can_modify(self, *args, **kwargs):
        return True
