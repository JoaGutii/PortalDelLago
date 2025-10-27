#!/usr/bin/env bash
python manage.py migrate
python manage.py loaddata fixtures/demo_users.json
python manage.py loaddata fixtures/demo_data.json
