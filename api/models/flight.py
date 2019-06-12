from .database import db
from .base.base_model import BaseModel


class Flight(BaseModel):
    """Class for flight's model"""

    __tablename__ = 'flights'

    airplane_id = db.Column(
        db.String, db.ForeignKey('airplanes.id'), nullable=False)
    flying_from = db.Column(db.String(400), nullable=False)
    flying_to = db.Column(db.String(400), nullable=False)
    departure = db.Column(db.DateTime, nullable=False)
    arrival = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        date = self.departure.date
        return (
            f'<Flight {self.flying_from} - {self.flying_to} ({date})>')
