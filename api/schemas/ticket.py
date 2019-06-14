"""Module for ticket schema"""
from marshmallow import fields

from .base.base_schema import BaseSchema
from .flight import FlightSchema
from .user import UserSchema

from ..utilities.helpers.common_schema_args import common_schema_args
from ..utilities.validators.string_length_validator import \
    string_length_validator, empty_string_validator


class TicketSchema(BaseSchema):
    """Schema for flight model"""
    user_id = fields.String(
        **common_schema_args(
            validate=(
                string_length_validator(60),
                empty_string_validator)),
        load_only=True)
    flight_id = fields.String(
        **common_schema_args(
            validate=(
                string_length_validator(60),
                empty_string_validator)),
        load_only=True)
    status = fields.Method('get_status_value', dump_only=True)
    user = fields.Nested(UserSchema, dump_only=True)
    flight = fields.Nested(FlightSchema, dump_only=True)

    def get_status_value(self, obj):
        """Returns the value of role retrieved from database"""
        return obj.status.value
