import logging
from typing import Tuple, Any, Optional, Callable, ClassVar, TypeVar, cast, Dict

import jwt
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.module_loading import import_string
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from api.authentication.services.jwt_authentication import CookieOrHeaderAuthentication


class Auth0JWTBearerTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"

    _jwks_client: ClassVar[Optional[jwt.PyJWKClient]] = None

    @staticmethod
    def get_setting(name, default):
        return getattr(settings, name, default)

    @classmethod
    def get_jwks_client(cls) -> jwt.PyJWKClient:
        if not cls._jwks_client:
            domain = cls.get_setting("AUTH0_DOMAIN", "")
            issuer = f"https://{domain}/"
            jsonurl = f"{issuer}.well-known/jwks.json"
            cls._jwks_client = jwt.PyJWKClient(
                jsonurl
            )
        return cls._jwks_client

    @classmethod
    def clear_jwks_cache(cls) -> None:
        cls._jwks_client = None

    def authenticate_credentials(self, key: str) -> Tuple[Any, dict]:
        try:
            token: dict = self.decode_token(key)
        except jwt.exceptions.PyJWTError as exc:
            raise exc
            # raise AuthenticationFailed("Invalid token")
        return (self.lookup_user(key, token), token)

    def decode_token(self, token: str) -> dict:
        print(token, "token")
        signing_key = self.get_jwks_client().get_signing_key_from_jwt(token)
        return jwt.decode(
            jwt=token,
            key=signing_key.key,
            algorithms=self.get_setting("DRF_PYJWT_ALGORITHMS", ["RS256"]),
            options=self.get_setting("DRF_PYJWT_OPTIONS", {}),
            **cast(Dict[str, Any], self.get_setting("DRF_PYJWT_KWARGS", {})),
        )

    @classmethod
    def lookup_user(cls, key: str, token: dict) -> Optional[AbstractBaseUser]:
        import_str = cls.get_setting("DRF_PYJWT_LOOKUP_USER", "")
        if import_str:
            # _lookup_user: Callable[[dict], Optional[AbstractBaseUser]]
            _lookup_user = import_string(import_str)
            return _lookup_user(key, token)
        return None


class DoubleAuthentication(TokenAuthentication):
    keyword = "Bearer"
    authenticator_classes = [
        Auth0JWTBearerTokenAuthentication, CookieOrHeaderAuthentication]

    def authenticate(self, *args, **kwargs) -> Tuple[Any, dict]:
        for authenticator_class in self.authenticator_classes:
            authenticator = authenticator_class()
            try:
                return authenticator.authenticate(*args, **kwargs)
            except jwt.exceptions.PyJWTError as exc:
                print("Error in double authentication", exc)
                continue
        raise AuthenticationFailed("Invalid token")
