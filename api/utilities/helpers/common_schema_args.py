from api.utilities.messages.serialization import serialization_messages


def common_schema_args(**kwargs):
    """ Returns the common arguments used in marshmallow fields.
    Args:
        kwargs: key word arguments use in fields
        ie validate=some_function

    Returns:
        dict: Resultant fields to be passed to a schema

    """

    return {
        "required": True,
        "validate": kwargs.get('validate'),
        "error_messages": {
            'required': serialization_messages['field_required']
        }
    }
