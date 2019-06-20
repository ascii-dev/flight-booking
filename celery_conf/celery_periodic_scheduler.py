"""Periodic tasks"""
from main import celery_app

celery_app.conf.beat_schedule = {}
