"""Module to validate endpoints only admin can access"""
from functools import wraps

from .base_validator import ValidationError
from ..messages.error import error_messages
from flask_jwt_extended import get_jwt_identity


def validate_admin_access(func):
    """Decorator function to check that only admin can access endpoint"""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        user = get_jwt_identity()
        if user['role'] != 'admin':
            raise ValidationError(
                {
                    'message': error_messages['not_allowed']
                }, 401)
        return func(*args, **kwargs)

    return decorated_function
