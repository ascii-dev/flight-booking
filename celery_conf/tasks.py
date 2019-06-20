"""Celery tasks"""
from main import celery_app


@celery_app.task(name="sample_scheduler")
def sample_scheduler():
    return dict(message="sample scheduler")
