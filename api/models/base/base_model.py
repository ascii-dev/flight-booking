"""Module for base model"""
import re

from datetime import datetime as dt

from api.utilities.validators.base_validator import ValidationError
from ..database import db


class BaseModel(db.Model):  # pragma: no cover
    """Class for base model attributes and method"""

    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True)
    created_at = db.Column(db.DateTime, default=dt.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=dt.utcnow)

    def save(self):
        """
        Saves a model instance
        :return: model instance
        """
        db.session.add(self)
        db.session.commit()
        return self

    def update(self, **kwargs):
        """
        Updates a mode instance
        :return: updated model instance
        """
        for field, value in kwargs.items():
            setattr(self, field, value)
            db.session.commit()

    def delete(self):
        """
        Deletes a database instance
        :return: None
        """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_or_404(cls, instance_id):
        """
        Gets an instance by id or returns 404
        :param instance_id: the id of instance to get
        :return: return instance or 404
        """
        instance = cls.query.filter_by(id=instance_id).first()
        if not instance:
            raise ValidationError(
                {
                    'message':
                    f'{re.sub(r"(?<=[a-z])[A-Z]+",lambda x: f" {x.group(0).lower()}" , cls.__name__)} not found'  # noqa
                },
                404)
        return instance
