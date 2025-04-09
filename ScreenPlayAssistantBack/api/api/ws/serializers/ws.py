# Rest Framework
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class WSSerializer(serializers.Serializer):
    """
    Serializer for subscribing to chat web socket
    """

    type = serializers.CharField(write_only=True)
    event_id = serializers.IntegerField(write_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs

    def get_group_names(self):
        groups = []
        if self.validated_data['type'] == 'event':
            groups.append('event-{}'.format(self.validated_data['event_id']))
        return groups
