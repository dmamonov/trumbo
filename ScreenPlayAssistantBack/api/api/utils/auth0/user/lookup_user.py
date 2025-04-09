from django.conf import settings
from django.db.models import Q
from api.users.models import User
from .create_from_token import create_from_token

import requests

"""
{
    'iss': 'https://dev-XXXXXXX.us.auth0.com/',
    'sub': 'google-oauth2|111111111111111111',
    'aud': [
        'https://dev-XXXXXXX.us.auth0.com/api/v2/',
        'https://dev-XXXXXXX.us.auth0.com/userinfo'
    ],
    'iat': 1654990327,
    'exp': 1655076727,
    'azp': 'XXXXXXXXXXXXXXXXXXXXX',
    'scope': 'openid profile email read:current_user'
}
"""


def lookup_user(key: str, token: dict):
    """Searches for the user email so it takes into
    account the users registered via email and password
    """
    auth0_id = token['sub'].split('|')[1]
    email = f"{auth0_id}@auto_generated.email"
    if 'email' in token:
        email = token['email']

    # need to check for the email or the auth0 id in case that the
    # user change his auto generated email, this is because the changed email
    # do not came in the token
    filters = Q(email=email) | Q(auth0_id=auth0_id)
    user_queryset = User.objects.filter(filters)

    if user_queryset:
        return user_queryset.first()
    return create_from_token(key, token)
