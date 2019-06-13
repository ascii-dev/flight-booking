"""Module for flight schema"""
from marshmallow import fields

from .base.base_schema import BaseSchema
from .airplane import AirplaneSchema

from ..utilities.helpers.common_schema_args import common_schema_args
from ..utilities.validators.string_length_validator import \
    string_length_validator, empty_string_validator


class FlightSchema(BaseSchema):
    """Schema for flight model"""
    airplane_id = fields.String(
        **common_schema_args(
            validate=(
                string_length_validator(60),
                empty_string_validator)),
        load_only=True)
    flying_from = fields.String(
        **common_schema_args(
            validate=(
                string_length_validator(250),
                empty_string_validator)),
        load_from="from",
        dump_to="from")
    flying_to = fields.String(
        **common_schema_args(
            validate=(
                string_length_validator(250),
                empty_string_validator)),
        load_from="to",
        dump_to="to")
    departure = fields.DateTime(**common_schema_args())
    arrival = fields.DateTime(**common_schema_args())
    airplane = fields.Nested(AirplaneSchema, dump_only=True)
