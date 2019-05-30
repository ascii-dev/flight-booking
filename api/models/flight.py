from .database import db
from .base.base_model import BaseModel


class Flight(BaseModel):
    """Class for flight's model"""
    airplane_id = db.Column(
        db.String, db.ForeignKey('airplane.id'), nullable=False)
    flying_from = db.Column(db.String(400), nullable=False)
    flying_to = db.Column(db.String(400), nullable=False)
    departure = db.Column(db.DateTime, nullable=False)
    arrival = db.Column(db.DateTime, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return (
            f'<Airplane {self.flying_from} - {self.flying_to} ({self.date})>')
