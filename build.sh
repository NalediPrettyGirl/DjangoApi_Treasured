#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
# Fake all migrations for store_api to sync the DB state
python manage.py migrate store_api --fake || true
python manage.py migrate
