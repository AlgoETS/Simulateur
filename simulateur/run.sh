#!/bin/bash

# Run migrations and seed the database
python manage.py makemigrations
python manage.py migrate
python manage.py seed_database

# Create a superadmin user
python manage.py createsuperadmin --username admin --password admin --noinput --email 'admin@admin.com'

python run.py --start-simulation 1
