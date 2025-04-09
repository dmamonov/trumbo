# Rest Framework
from rest_framework import serializers

# Utilities
from api.authentication.services.jwt_authentication import CookieOrHeaderAuthentication


# Models


class WSSerializer(serializers.Serializer):
    """
    Serializer for subscribing to chat web socket
    """

    TOKEN = serializers.CharField(write_only=True)
    type = serializers.CharField(write_only=True, default='events')

    def validate(self, attrs):
        attrs = super().validate(attrs)

        # Authenticate token
        token = attrs['TOKEN']
        user, _ = CookieOrHeaderAuthentication().get_user_from_token(token)
        attrs['user'] = user

        return attrs

    def get_group_names(self):
        chats = []

        if self.validated_data['type'] == 'events':
            chats.append(f"event-{self.validated_data['user'].id}")

        return chats
