"""
Events Views
"""

# Django
from django.utils import timezone
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
# Rest Framework
from rest_framework.viewsets import GenericViewSet

# Models
from api.events.models import UserEvent
# Serializers
from api.events.serializers import UserEventSerializer
from api.users.permissions import IsValidUserPermission
# Utilities
from api.utils.views import BaseViewSet


class EventViewSet(BaseViewSet, mixins.ListModelMixin, GenericViewSet):
    queryset = UserEvent.objects.exclude(deleted=True)
    serializer_class = UserEventSerializer
    permission_classes = [IsValidUserPermission]
    lookup_field = 'event'

    def get_queryset(self):
        """This will add filters to get unseen Events from the User Events"""

        queryset = super().get_queryset().filter(user=self.request.user)

        if bool(self.request.query_params.get('unseen')):
            return queryset.filter(seen_at=None)

        return queryset

    @action(detail=False, methods=['post'])
    def mark_as_read(self, request, **kwargs):
        """Mark event as read"""

        now = timezone.now()
        user_events = self.get_queryset().filter(user=request.user)
        user_events.update(seen_at=now)
        return Response({"success": True})
