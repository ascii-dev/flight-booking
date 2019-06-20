"""Celery worker configuration"""
from main import celery_app, create_app  # noqa: F401

app = create_app()

app.app_context().push()
