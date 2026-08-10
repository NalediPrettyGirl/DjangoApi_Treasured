#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input

# Fake up to 0005 (because your DB already has those columns), then apply the rest normally!
python manage.py migrate store_api 0005 --fake || true
python manage.py migrate
