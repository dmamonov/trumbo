from django.conf import settings
from django.core.mail import send_mail


def send_email_message(message, title, language_code=None, email=None, **kwargs):
    from_email = settings.EMAIL_NO_REPLY
    send_mail(title, message=message, from_email=from_email,
              recipient_list=[email], fail_silently=False)
