from django.db import models
from django.utils.translation import gettext_lazy as _


class SetUpStatus(models.IntegerChoices):
    SIGN_UP_VALIDATION = 0, _('Sign Up Validation')
    VALIDATED = 1, _('Validated')


class PasswordStatus(models.IntegerChoices):
    CHANGE = 0, _('Requires password Change')
    ACTIVE = 1, _('ACTIVE')
    EXTERNAL = 2, _('External')
