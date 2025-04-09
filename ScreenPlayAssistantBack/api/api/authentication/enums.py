from django.utils.translation import gettext_lazy as _
from django.db import models


class ExternalTokenChannel(models.IntegerChoices):
    CONSOLE = 0, _('Console')
    SMS = 1, _('SMS')
    EMAIL = 2, _('Email')
    __empty__ = _('(Unknown)')


class ExternalTokenType(models.IntegerChoices):
    VALIDATE_ACCOUNT = 1, _('Validate account')
    RECOVER_ACCOUNT = 2, _('Recover account')

    __empty__ = _('(Unknown)')
