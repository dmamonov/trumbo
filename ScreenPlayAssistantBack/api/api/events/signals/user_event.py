"""User Events Signals"""

# Channels
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
# Django
from django.dispatch import receiver

# Models
from api.events.models import UserEvent, Event
# Serializers
from api.events.serializers import UserEventSerializer
# Utilities
from api.utils.web_socket import send_message


@receiver(post_save, sender=UserEvent)
def send_web_socket_message(sender, instance, created, **kwargs):
    if not instance.user:
        return
    if created:
        try:
            serializer = UserEventSerializer(instance)
            print(f"event-{instance.user.id}")
            async_to_sync(send_message)(f"event-{instance.user.id}", dict(serializer.data),
                                        str(serializer.data['event']['type']))
        except Event.DoesNotExist as e:
            pass
