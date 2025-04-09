from pytz import timezone as pztimezone
from django.conf import settings

def proper_date(date):
    settings_time_zone = pztimezone(settings.TIME_ZONE)
    return date.astimezone(settings_time_zone).strftime('%d %B, %Y %I:%M %p')
