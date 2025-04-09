# Django
from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
# Timezone
from django.utils import timezone

from api.events.enums import EventType
from api.events.service.event_service import EventService
# Models
from api.users.models import User
# Utils
from api.utils.models import BaseModel

# Channels

timezone.activate(settings.TIME_ZONE)


class UserEvent(BaseModel):
    """
    User event model
    """

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    event = models.ForeignKey(
        'events.Event', on_delete=models.CASCADE, related_name='user_events')
    seen_at = models.DateField(null=True, blank=True, default=None)
    amount = models.IntegerField(default=1)

    @property
    def event_type(self):
        event_type = self.event.type
        return event_type


class Event(BaseModel):
    """
    Event model
    """

    type = models.CharField(choices=EventType.choices, max_length=10)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @classmethod
    def test(cls, created_by):
        # Create Test Event
        event, _ = cls.objects.get_or_create(type=EventType.TEST, created_by=created_by)
        UserEvent.objects.create(user=created_by, event=event)
        EventService().send_test_event(created_by)
        return event
