"""Periodic tasks"""
from celery.schedules import crontab

from main import celery_app

celery_app.conf.beat_schedule = {
    'run-travel-reminder-automatically-every-day': {
        'task': 'travel_reminder',
        'schedule': crontab(hour=7, minute=0)
    },
}
