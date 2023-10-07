#!/bin/bash
set -e

while ! nc -z db 5432; do
  sleep 0.1
done

echo "Running migrations"

python manage.py makemigrations
python manage.py migrate

echo "Loading fixtures"

python manage.py loaddata fixtures/db.json

exit 0
