"""Module for airplane schema"""
from marshmallow import fields


from .base.base_schema import BaseSchema

from ..utilities.helpers.common_schema_args import common_schema_args
from ..utilities.validators.string_length_validator import \
    string_length_validator, empty_string_validator
from ..utilities.validators.name_validator import name_validator


class AirplaneSchema(BaseSchema):
    """Schema for airplane model"""
    model = fields.String(
        **common_schema_args(validate=(
            name_validator,
            string_length_validator(60),
            empty_string_validator)))
    brand = fields.String(
        **common_schema_args(validate=(
            name_validator,
            string_length_validator(60),
            empty_string_validator)))
    capacity = fields.Integer(
        **common_schema_args())
