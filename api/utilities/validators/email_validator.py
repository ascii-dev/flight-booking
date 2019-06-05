""" Module with email validator. """
import re

from marshmallow import ValidationError
from ..messages.serialization import serialization_messages

EMAIL_REGEX = re.compile(
    r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b", re.I | re.UNICODE)


def email_validator(data):
    """
    Checks if given string is at least 1 character and only contains characters
    that make a valid email address.
    """

    data = data.lower()

    # Check if email pattern is matched
    if not EMAIL_REGEX.match(data):
        raise ValidationError(
            serialization_messages['invalid_email'])
