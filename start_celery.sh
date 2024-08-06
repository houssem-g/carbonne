#!/bin/bash

# Start Celery Beat
echo "Starting Celery Beat..."
poetry run celery -A app.core.celery_app beat --loglevel=info &

# Start Celery Workers
echo "Starting Celery Workers..."
celery -A app.core.celery_app worker --loglevel=info --concurrency=5
