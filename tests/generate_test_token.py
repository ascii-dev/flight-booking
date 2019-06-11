from api.utilities.helpers.generate_token import generate_token
from api.utilities.messages.serialization import serialization_messages
from api.utilities.validators.base_validator import ValidationError


def generate_test_token(user=None):
    if user:
        return generate_token(user)
    raise ValidationError({
        "message": serialization_messages['not_empty']
    })
