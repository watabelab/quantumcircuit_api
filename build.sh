#!/usr/bin/env bash
# exit on error
set -o errexit

#/opt/render/project/src/.venv/bin/python3.8 -m pip install --upgrade pip

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py superuser
