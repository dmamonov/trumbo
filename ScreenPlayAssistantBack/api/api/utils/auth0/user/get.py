from django.conf import settings
import requests

def get_user(key:str, user_sub:dict):
    headers = { 'authorization': f"Bearer {key}" }

    res = requests.request("GET", f"https://{settings.AUTH0_DOMAIN}/api/v2/users/{user_sub}", headers=headers)
    data = res.json()
    return data

"""
Auth0 user description call example response
{
    'created_at': '2022-06-09T01:56:54.146Z',
    'email': 'yersonlasso05@gmail.com',
    'email_verified': True,
    'family_name': 'Lasso',
    'given_name': 'Yerson',
    'identities': [
        {'provider': 'google-oauth2', 'user_id': '101571016880604136081', 'connection': 'google-oauth2', 'isSocial': True}
        ],
    'locale': 'es-419',
    'name': 'Yerson Lasso',
    'nickname': 'yersonlasso05',
    'picture': 'https://lh3.googleusercontent.com/a-/AOh14Ghd3OywYaI_b-wlLfYJjQtUkIjmzyW2Aa3-YQac7Q=s96-c',
    'updated_at': '2022-06-11T23:10:53.263Z',
    'user_id': 'google-oauth2|101571016880604136081',
    'last_ip': '186.84.91.40',
    'last_login': '2022-06-11T23:10:53.262Z',
    'logins_count': 13
}
"""