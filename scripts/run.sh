#!/bin/bash

poetry run alembic upgrade head || exit 1

poetry run python3 main.py

poetry run celery -A app.celery_worker worker

poetry run celery -A app.celery_worker flower
