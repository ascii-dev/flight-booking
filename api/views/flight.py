"""Module that holds flight endpoints"""
from flask import request
from flask_jwt_extended import jwt_required
from flask_restplus import Resource

from api.models import Airplane
from main import api

from ..models.flight import Flight
from ..utilities.messages.success import success_messages
from ..utilities.validators.base_validator import ValidationError
from ..utilities.messages.serialization import serialization_messages
from ..utilities.validators.validate_json_request import validate_json_request
from ..utilities.validators.validate_admin_access import validate_admin_access
from ..schemas.flight import FlightSchema


@api.route('/airplanes/<string:airplane_id>/flights')
class FlightsResource(Resource):
    """Resource for flight creation"""

    @jwt_required
    @validate_json_request
    @validate_admin_access
    def post(self, airplane_id):
        """
        Create a new flight record schedule in the database
        :return: status, success message and relevant flight details
        """
        request_data = request.get_json()
        Airplane.get_or_404(airplane_id)
        request_data['airplane_id'] = airplane_id

        schema = FlightSchema()
        flight_data = schema.load_object_into_schema(request_data)

        flight = Flight(**flight_data)
        flight.save()
        flight_dump = schema.dump(flight).data
        flight_dump['date'] = flight.departure.date().strftime("%Y-%m-%d")

        return {
            "status": "success",
            "message": success_messages['created'].format('Flight'),
            "data": flight_dump,
        }, 201
