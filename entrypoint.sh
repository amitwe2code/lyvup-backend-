# #!/bin/sh

# # Wait for postgres
# while ! nc -z postgres-db 5432; do
#   echo "Waiting for postgres..."
#   sleep 1
# done

# echo "PostgreSQL started"

# python manage.py migrate
# python manage.py runserver 0.0.0.0:8000