from .database import db
from .base.base_model import BaseModel


class Airplane(BaseModel):
    """Class for airplane's model"""

    __tablename__ = 'airplanes'

    brand = db.Column(db.String(60), nullable=False)
    model = db.Column(db.String(60), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Airplane {self.brand} {self.model} {self.capacity}>'
