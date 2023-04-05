#!/usr/bin/env bash
set -u   # crash on missing env variables
set -e   # stop on any error
set -x

rm -rf /static/*

echo Test cache
python manage.py test_cache

exec python -m debugpy --listen 0.0.0.0:5678 /app/manage.py runserver 0.0.0.0:8000
