"""Module for sending email"""
from flask import current_app
from flask_mail import Message, Mail
from celery import Celery

from config import AppConfig

celery_scheduler = Celery(__name__, broker=AppConfig.CELERY_BROKER_URL)
celery_scheduler.conf.enable_utc = False


class FlaskMailSender:
    """Class for sending emails using FlaskMail"""

    @classmethod
    @celery_scheduler.task(name='send_email')
    def send_mail(cls, recipients, subject, body):
        """Method to send the email"""
        with current_app.app_context():
            flask_mail = Mail(current_app)
            message = {
                'subject': subject,
                'recipients': recipients,
                'html': body,
            }

        return flask_mail.send(Message(**message))
