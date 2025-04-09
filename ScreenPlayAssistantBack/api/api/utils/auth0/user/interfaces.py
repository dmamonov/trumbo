from api.users.models import User
from api.utils.auth0.user import get_user

OWNER_PUBLIC_KEYS = [
    'created_at',
    'email',
    'email_verified',
    'family_name',
    'given_name',
    'identities',
    'name',
    'nickname',
    'picture',
    'updated_at',
    'last_login',
]

class Auth0User:
    _user:User
    data:dict

    def __init__(self, key:str, sub:str, user:User):
        self._user = user
        self._get_data(key, sub)

    def _get_data(self, key:str, sub:str):
        auth0_user_data = get_user(key, sub)
        
        user_data = { k: auth0_user_data[k] for k in OWNER_PUBLIC_KEYS }

        user_data['identities'] = [identitie['provider'] for identitie in user_data['identities']]

        self.data = user_data
