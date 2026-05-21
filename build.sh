#!/usr/bin/env bash

pip install --upgrade pip setuptools wheel

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate