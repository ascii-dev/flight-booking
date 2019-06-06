"""Module for user schema"""
from marshmallow import fields

from api.utilities.messages.serialization import serialization_messages
from .base.base_schema import BaseSchema

from ..utilities.helpers.common_schema_args import common_schema_args
from ..utilities.validators.string_length_validator import \
    string_length_validator, empty_string_validator, min_length_validator
from ..utilities.validators.name_validator import name_validator
from ..utilities.validators.email_validator import email_validator


class UserSchema(BaseSchema):
    """Schema for user model"""
    first_name = fields.String(
        **common_schema_args(validate=(
            name_validator,
            string_length_validator(60),
            empty_string_validator)),
        load_from="firstName",
        dump_to="firstName")
    last_name = fields.String(
        **common_schema_args(validate=(
            name_validator,
            string_length_validator(60),
            empty_string_validator)),
        load_from="lastName",
        dump_to="lastName")
    email = fields.String(
        **common_schema_args(validate=email_validator))
    role = fields.Method('get_role_value', dump_only=True)
    passport_photograph = fields.Dict(
        dump_only=True,
        dump_to="passport",
        error_messages={'required': serialization_messages['field_required']})
    password = fields.String(
        **common_schema_args(validate=(
            string_length_validator(60),
            empty_string_validator,
            min_length_validator)),
        load_only=True)

    def get_role_value(self, obj):
        """Returns the value of role retrieved from database"""
        return obj.role.value
