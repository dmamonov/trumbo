# Rest Framework
def user_jwt_setting(set_cookie, jwt_settings, is_refresh=False, refresh_token=None, access_token=None):
    # build your response and set cookie
    set_cookie(
        key = jwt_settings['ACCESS_TOKEN_COOKIE'], 
        value = access_token,
        expires = jwt_settings['ACCESS_TOKEN_LIFETIME'],
        secure = jwt_settings['ACCESS_TOKEN_COOKIE_SECURE'],
        httponly = jwt_settings['ACCESS_TOKEN_COOKIE_HTTP_ONLY'],
        samesite = jwt_settings['ACCESS_TOKEN_COOKIE_SAMESITE']
    )
    if not is_refresh:
        set_cookie(
            key = jwt_settings['REFRESH_TOKEN_COOKIE'], 
            value = refresh_token,
            expires = jwt_settings['REFRESH_TOKEN_LIFETIME'],
            secure = jwt_settings['REFRESH_TOKEN_COOKIE_SECURE'],
            httponly = jwt_settings['REFRESH_TOKEN_COOKIE_HTTP_ONLY'],
            samesite = jwt_settings['REFRESH_TOKEN_COOKIE_SAMESITE']
        )

    tokens = dict()
    if access_token:
        tokens[jwt_settings['ACCESS_TOKEN_COOKIE']] = access_token
    if refresh_token:
        tokens[jwt_settings['REFRESH_TOKEN_COOKIE']] = refresh_token
    return tokens
