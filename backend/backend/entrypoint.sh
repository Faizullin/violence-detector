#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
done

echo "PostgreSQL started"

echo "Running migrations..."
python3 manage.py makemigrations --settings=backend.settings.local
echo "Migrations complete"

# echo "Running migrate..."
# python3 manage.py migrate --settings=backend.settings.local
# echo "Migrate complete"


exec "$@"
