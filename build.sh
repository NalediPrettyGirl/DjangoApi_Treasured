#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
# Fake migration 0004 to fix the "already exists" error on Render
python manage.py migrate store_api 0004 --fake || true
python manage.py migrate
