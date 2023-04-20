FROM python:3.11-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code
COPY . /code

RUN apt-get update && \
    apt-get install -y gcc vim postgresql-client nginx && \
    apt-get remove --purge --auto-remove -y

COPY nginx/nginx.conf /etc/nginx/sites-enabled/default

RUN pip install -r requirements.txt && \
    python manage.py collectstatic --noinput

CMD [ "bash", "./scripts/run.sh" ]
