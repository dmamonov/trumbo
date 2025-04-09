# Django
from django.db import models
from django.utils.translation import gettext_lazy as _


class ContentType(models.TextChoices):
    TEXT = 'T', _('Text')
    NUMBER = 'N', _('Number')
    IMAGE = 'I', _('Image')
    JSON = 'J', _('Json')


class Content(models.Model):
    """
    Content model
    """
    # name unique
    name = models.CharField(max_length=255, unique=True)
    content_text = models.TextField(null=True, blank=True)
    content_image = models.ImageField(null=True, blank=True, upload_to ='content/%Y/%m/%d/')
    content_number = models.DecimalField(null=True, blank=True, max_digits=19, decimal_places=10)
    content_json = models.JSONField(null=True, blank=True)
    content_type = models.CharField(choices=ContentType.choices, default=ContentType.TEXT, max_length=5, null=False, blank=False)
    
    @property
    def content(self):
        if self.content_type == ContentType.NUMBER:
            return self.content_number
        elif self.content_type == ContentType.IMAGE:
            return self.content_image.url
        elif self.content_type == ContentType.TEXT:
            return self.content_text
        elif self.content_type == ContentType.JSON:
            return self.content_json

    def get_traduction(self, language):
        if self.content_type not in [ContentType.TEXT]:
            return self.content
        attr_name = f'content_text_{language}'
        if hasattr(self, attr_name):
            return self.content_text
        traduction = getattr(self, attr_name)
        return traduction
