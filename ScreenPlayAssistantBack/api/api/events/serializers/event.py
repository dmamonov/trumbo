# Rest Framework
import dateutil.relativedelta
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.events.enums import EventType
# Models
from api.events.models import Event, UserEvent
# utilities
from api.users.models import User
from api.utils.serializers import ChoiceField


# Django
class UserForEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "id", "profile_picture", "first_name"]


class SimpleUserEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEvent
        fields = ['event_type']


class EventsModelSerializer(serializers.ModelSerializer):
    type = ChoiceField(choices=EventType.choices)
    is_checked = serializers.SerializerMethodField()

    def get_is_checked(self, obj):
        return obj.user_events.exclude(seen_at=None).exists()

    class Meta:
        model = Event
        fields = ['id', 'type', 'created_by', 'created', 'is_checked']


class UserEventSerializer(SimpleUserEventSerializer):
    event = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()
    section = serializers.SerializerMethodField()

    class Meta:
        model = UserEvent
        fields = ['event', 'data', 'section']

    def get_section(self, obj):
        last_week = (now() + dateutil.relativedelta.relativedelta(weeks=-1)).date()
        last_month = (now() + dateutil.relativedelta.relativedelta(months=-1)).date()
        today = now().date()
        event_created_date = obj.event.created.date()

        if event_created_date == today:
            return "today"
        if today >= event_created_date >= last_week:
            return "last_week"
        if last_week >= event_created_date >= last_month:
            return "last_month"

    def to_representation(self, instance):
        repr = super(UserEventSerializer, self).to_representation(instance)
        if repr['section'] == "today":
            repr['order'] = 1
        if repr['section'] == "last_week":
            repr['order'] = 2
        if repr['section'] == "last_month":
            repr['order'] = 3

        data = repr.pop("data")
        final_data = {**repr, **data}
        return final_data

    def get_data(self, obj):
        EVENT_SERIALIZERS_BY_TYPE = {
            # EventType.COMMENT_REPLY: UserEventCommentWithChildModelSerializer,
        }
        event_type = obj.event_type
        if obj.event_type not in EVENT_SERIALIZERS_BY_TYPE:
            raise ValidationError(
                f'The event type {event_type.name} is not supported')

        serializer = EVENT_SERIALIZERS_BY_TYPE[event_type](obj)
        return serializer.data

    def get_event(self, obj):
        event = obj.event
        serializer = EventsModelSerializer(event)
        return serializer.data
