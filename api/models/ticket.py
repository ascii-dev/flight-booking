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

    def __repr__(self):
        return f'<Ticket {self.status}>'
