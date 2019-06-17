from .database import db
from .base.base_model import BaseModel

from ..utilities.enums import TicketStatusEnum


class Ticket(BaseModel):
    """Class for ticket's model"""

    __tablename__ = 'tickets'

    user_id = db.Column(
        db.String, db.ForeignKey('users.id'), nullable=False)
    flight_id = db.Column(
        db.String, db.ForeignKey('flights.id'), nullable=False)
    status = db.Column(
        db.Enum(TicketStatusEnum),
        nullable=False,
        default='pending')

    user = db.relationship(
        'User',
        backref='user',
        primaryjoin="and_(Ticket.user_id==User.id)")
    flight = db.relationship(
        'Flight',
        backref='flight',
        primaryjoin="and_(Ticket.flight_id==Flight.id)")

    def __repr__(self):
        return f'<Ticket {self.status}>'
