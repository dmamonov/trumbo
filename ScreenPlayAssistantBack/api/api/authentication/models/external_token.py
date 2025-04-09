# Utilities
from api.authentication.services.external_token.token import random_token
from api.authentication.services.external_token.channels import send_token
from django.utils.timezone import now
from api.authentication.enums import ExternalTokenChannel, ExternalTokenType
from django.conf import settings

# Models
from api.utils.models import BaseModel
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class ExternalToken(BaseModel):
    channel = models.IntegerField(
        choices=ExternalTokenChannel.choices,
        default=ExternalTokenChannel.SMS,
    )
    type = models.IntegerField(
        choices=ExternalTokenType.choices,
        blank=False
    )
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='external_token', null=False,
                             blank=False)
    token = models.CharField(default=random_token, max_length=16, blank=True)

    @classmethod
    def get_token_type_lifetime(cls, token_type):
        return settings.AUTHENTICATION_EXTERNAL_TOKEN_EXPIRY[cls.get_type_verbose(token_type).lower()]

    @classmethod
    def get_token_type_resend_time(cls, token_type):
        return settings.AUTHENTICATION_EXTERNAL_TOKEN_RESEND[cls.get_type_verbose(token_type).lower()]

    def get_channel_token_message(self):
        return settings.AUTHENTICATION_EXTERNAL_TOKEN_FORMATS[self.channel_verbose.lower()][
            self.type_verbose.lower()].format(app_name=settings.APP_NAME, token=self.token)

    @classmethod
    def get_type_verbose(cls, token_type):
        return ExternalTokenType._value2member_map_[token_type]._name_

    def get_message_details(self):
        if self.channel_verbose.lower() not in settings.AUTHENTICATION_EXTERNAL_TOKEN_MESSAGE_FORMATS:
            message = self.token
        else:
            format_values = {
                "app_name": settings.APP_NAME, "token": self.token}
            if self.channel_verbose.lower() == 'email':
                format_values["email"] = self.user.email

            message = settings.AUTHENTICATION_EXTERNAL_TOKEN_MESSAGE_FORMATS[self.channel_verbose.lower()][
                self.type_verbose.lower()].format(**format_values)

        if self.channel_verbose.lower() not in settings.AUTHENTICATION_EXTERNAL_TOKEN_TITLE_FORMATS:
            title = None  # self.get_type_verbose().lower()
        else:
            title = settings.AUTHENTICATION_EXTERNAL_TOKEN_TITLE_FORMATS[self.channel_verbose.lower()][
                self.type_verbose.lower()].format(app_name=settings.APP_NAME, message_type=self.type_verbose)

        return message, title

    @property
    def type_verbose(self):
        return self.get_type_verbose(self.type)

    @property
    def channel_verbose(self):
        return ExternalTokenChannel._value2member_map_[self.channel]._name_

    @classmethod
    def get_valid_tokens(cls, field, token_type):
        token_life_time = cls.get_token_type_lifetime(token_type)
        token_validity_range = now() - token_life_time
        return cls.objects.filter(
            **field,
            created__gte=token_validity_range,
            type=token_type,
        )

    @property
    def resend_at(self):
        return self.created + self.get_token_type_resend_time(self.type)

    @property
    def expires_at(self):
        return self.created + self.get_token_type_lifetime(self.type)

    @property
    def is_expired(self):
        return self.expires_at < now()


@receiver(post_save, sender=ExternalToken)
def auth_token_created(sender, instance: ExternalToken, *args, **kwargs):
    try:
        channel_token_message, channel_token_title = instance.get_message_details()
        send_token(instance.type_verbose, instance.channel_verbose,
                   instance.user.preferred_language_code, email=instance.user.email, phone_number=instance.user.phone_number, channel_token_message=channel_token_message, channel_token_title=channel_token_title)
    except Exception as e:
        raise e
