"""Events models admin."""

# Django
from django.contrib import admin

# Models
from api.events.models import *


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'type',
        'created_by',
    )


@admin.register(UserEvent)
class UserEventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'event',
        'seen_at',
        'event_type',
    )