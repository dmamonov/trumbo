from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from rest_framework_simplejwt.serializers import RefreshToken


class CookieOrHeaderAuthentication(JWTAuthentication):

    def authenticate(self, request):
        header = self.get_header(request)

        if header is None:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT['ACCESS_TOKEN_COOKIE']) or None
        else:
            raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        return self.get_user_from_token(raw_token)
    
    def get_user_from_token(self, raw_token):
        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token 


def django_user_jwt(user):
    refresh = RefreshToken.for_user(user)
    return dict(
        refresh = str(refresh),
        access = str(refresh.access_token),
    )
