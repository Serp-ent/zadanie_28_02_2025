#!/bin/sh

# Exit on error
set -e

echo "Running migrations..."
python manage.py migrate --noinput

# echo "Collecting static files..."
# python manage.py collectstatic --noinput

echo "Ensuring default admin user (admin:admin) exists..."
python manage.py shell -c '
from django.contrib.auth.models import User;
try:
    User.objects.get(username="admin");
    print("admin user exists.");
except User.DoesNotExist:
    User.objects.create_superuser("admin", "admin@example.com", "admin");
    print("Created admin superuser.");
'

echo "Starting Django app..."
exec "$@"
