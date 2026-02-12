#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Running migrations..."
python manage.py migrate

echo "Initializing admin user..."
python manage.py init_admin

echo "Starting Gunicorn..."
gunicorn ticketera_project.wsgi:application
