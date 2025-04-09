from enum import Enum
from api.users.enums import SetUpStatus, PasswordStatus
from api.users.models import User
from api.authentication.enums import ExternalTokenType
from api.authentication.models import ExternalToken


# class SetUpStatus(Enum):
#     SIGN_UP_VALIDATION = 0
#     VALIDATED = 1


def destroy_token_by(phone_number=None, email=None, token_type=ExternalTokenType.VALIDATE_ACCOUNT):
    queryset = ExternalToken.objects.filter(
        type=token_type)

    if type(phone_number) is not None:
        queryset = queryset.filter(user__phone_number=phone_number)

    if type(email) is not None:
        queryset = queryset.filter(user__email=email)

    queryset.delete()


def create_token(user_id, channel, token_type=ExternalTokenType.VALIDATE_ACCOUNT):
    token = ExternalToken.objects.create(
        type=token_type, user_id=user_id, channel=channel)
    return token.resend_at, token.expires_at


def create_user(*args, **kwargs):
    user = User.objects.create_user(*args, **kwargs)
    return user.id


def signup_request_code(
    email,
    resend,
    channel,
    user_id,
):
    if not resend:
        user_id = create_user(email=email)
    else:
        destroy_token_by(email=email)
    create_token(user_id=user_id, channel=channel)
    return {
        'channel': channel,
        'resend': resend,
    }


def signup_validated(
    user: User,
):
    ExternalToken.objects.filter(
        user=user, type=ExternalTokenType.VALIDATE_ACCOUNT).delete()
    user.setup_status = SetUpStatus.VALIDATED
    user.password_status = PasswordStatus.ACTIVE
    user.save()
    return True


def signup_completed(
    set_user_setup_status,
    user_id,
):
    set_user_setup_status(user_id, SetUpStatus.VALIDATED)
    return True


def forgot_password_request_code(
    resend,
    channel,
    user_id,
    email=None,
    **kwargs,
):
    if resend:
        destroy_token_by(
            email=email, token_type=ExternalTokenType.RECOVER_ACCOUNT)
    create_token(user_id=user_id, channel=channel,
                 token_type=ExternalTokenType.RECOVER_ACCOUNT)
    return {
        'channel': channel,
        'resend': resend,
    }


def forgot_password_validated(
    user: User,
):
    ExternalToken.objects.filter(
        user=user, type=ExternalTokenType.RECOVER_ACCOUNT).delete()
    user.password_status = PasswordStatus.CHANGE
    user.save()
    return True
