from .sms import send_sms_message
from .console import send_console_message
from .email import send_email_message


CHANNELS = {
    "sms": send_sms_message,
    "console": send_console_message,
    "email": send_email_message,
}


def send_token(token_type, channel, token='', phone_number=None, email=None, channel_token_message=None, channel_token_title=None, language_code="en_US"):
    token_type = token_type.lower()
    channel = channel.lower()
    if channel not in CHANNELS:
        raise Exception(f'channel "{channel}" not supported')

    if channel_token_message:
        message = channel_token_message
    else:
        message = token
    return CHANNELS[channel](message, language_code=language_code, phone_number=phone_number, email=email, title=channel_token_title)
