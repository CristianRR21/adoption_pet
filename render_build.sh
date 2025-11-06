#!/usr/bin/env bash
# Script de despliegue para Render
python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
