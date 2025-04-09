from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRoles(models.TextChoices):
    ADMIN = 'A', _('Admin')
    SUPPORT = 'SP', _('Support')
    STANDARD = 'ST', _('Standard')
