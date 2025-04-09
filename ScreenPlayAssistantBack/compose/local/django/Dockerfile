FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev libxslt-dev \
  && apk add postgresql-dev \
  && apk add postgresql-client \
  # CFFI dependencies
  && apk add libffi-dev py-cffi \
  # Translations dependencies
  && apk add gettext \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev libjpeg
        
# Requirements are installed here to ensure they will be cached.
RUN apk add python3-dev
RUN apk add postgresql-client

COPY ./requirements /requirements
RUN pip install --upgrade pip
RUN pip install -r /requirements/local.txt

COPY ./compose/production/django/wait_for_postgres.py /wait_for_postgres.py
# RUN chmod +x /wait_for_postgres.py

COPY ./compose/local/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY ./compose/local/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

WORKDIR /app

# ENTRYPOINT ["/start"]
