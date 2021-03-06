"""Module to validate request content type"""
from functools import wraps
from flask import request

from .base_validator import ValidationError
from ..messages.serialization import serialization_messages


def validate_json_request(func):
    """Decorator function to check for json content type in request"""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            raise ValidationError(
                {
                    'status': 'error',
                    'message': serialization_messages['json_type_required']
                }, 400)
        return func(*args, **kwargs)

    return decorated_function
