#!/bin/sh

python manage.py migrate --noinput

python manage.py collectstatic --noinput

exec gunicorn main_app.wsgi:application --bind 0.0.0.0:8088 --workers 5