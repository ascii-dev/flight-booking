"""Celery tasks"""
from datetime import datetime as dt, timedelta

from flask import render_template
from sqlalchemy import func
import cloudinary

from api.models import Ticket, Flight
from api.utilities.email import FlaskMailSender
from main import celery_app


@celery_app.task(name="sample_scheduler")
def sample_scheduler():
    return dict(message="sample scheduler")


@celery_app.task(name="travel_reminder")
def travel_reminder():
    """Reminds users about their travels a day
    before the actual travel date"""
    tomorrow = (dt.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    tomorrows_tickets = Ticket.query.join(Flight).filter(
        func.DATE(Flight.departure) == tomorrow).all()

    for ticket in tomorrows_tickets:
        data = dict(
            first_name=ticket.user.first_name,
            last_name=ticket.user.last_name)
        email_body = render_template(
            '/email/travel_reminder.html',
            data=data)
        FlaskMailSender.send_mail(
            recipients=[ticket.user.email],
            subject="Travel reminder",
            body=email_body)


@celery_app.task(name="delete_passport")
def delete_passport(public_id):
    """Deletes a user's passport from cloudinary once
    it gets deleted locally
    :param public_id: the id of image to be deleted
    """
    cloudinary.api.delete_resources([public_id])
