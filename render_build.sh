#!/usr/bin/env bash
# Script de despliegue para Render (Django)

set -o errexit  # Detiene el script si ocurre un error

echo "📦 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🧱 Ejecutando migraciones..."
python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "✅ Despliegue completado correctamente"
