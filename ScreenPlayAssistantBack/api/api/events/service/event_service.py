from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from api.users.models import User


class EventService:
    def send_test_event(self, user: User):
        # if user.send_test_email:
        from_email = settings.EMAIL_NO_REPLY
        msg_plain = render_to_string('events/test.html', {})
        send_mail('Test', message="", from_email=from_email, recipient_list=[user.email],
                  html_message=msg_plain)
