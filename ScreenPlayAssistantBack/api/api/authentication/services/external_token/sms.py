from django.conf import settings

def send_sms_twilio(phone_number, message, language_code=None):
    from twilio.rest import Client
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        to=phone_number, 
        from_=settings.TWILIO_FROM_PHONE_NUMBER,
        body=message)

SMS_PROVIDERS = dict(
    twilio = send_sms_twilio
)

def send_sms_message(phone_number, message, language_code=None):
    if settings.SMS_PROVIDER not in SMS_PROVIDERS:
        raise Exception(f'sms provider "{settings.SMS_PROVIDER}" not supported')
    SMS_PROVIDERS[settings.SMS_PROVIDER](phone_number=phone_number, message=message, language_code=language_code)
