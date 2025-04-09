"""User models admin."""

# Django
from django.contrib import admin

# Models
from .models import *

@admin.register(ExternalToken)
class ExternalTokenAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'channel',
        'type',
        'user',
    )
