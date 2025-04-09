FROM python:3.7-alpine

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

COPY ./requirements /requirements
RUN pip install -r /requirements/production.txt

COPY ./compose/production/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY ./api ./app

WORKDIR /app
RUN mkdir -p ./api/static

ENTRYPOINT ["/start"]
