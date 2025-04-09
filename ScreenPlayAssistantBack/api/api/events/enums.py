from django.db import models
from django.utils.translation import gettext_lazy as _


class EventType(models.TextChoices):
    TEST = 'T', _('Test')
