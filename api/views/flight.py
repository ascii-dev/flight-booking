"""Module that holds flight endpoints"""
from datetime import datetime as dt

from flask import request
from flask_jwt_extended import jwt_required
from flask_restplus import Resource

from api.models import Airplane
from api.utilities.helpers.return_value import return_value
from main import api

from ..models.flight import Flight
from ..utilities.messages.success import success_messages
from ..utilities.validators.validate_json_request import validate_json_request
from ..utilities.validators.validate_admin_access import validate_admin_access
from ..schemas.flight import FlightSchema


@api.route('/airplanes/<string:airplane_id>/flights')
class AirplaneFlightsResource(Resource):
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

        return return_value(message=success_messages[
                                'created'].format('Flight'),
                            status="success",
                            data=schema.dump(flight).data,
                            status_code=201)


@api.route('/flights')
class FlightsResource(Resource):
    """Resource for flight """

    def get(self):
        """Get all flight records in the database that are
        still available to be booked
        :return: status, success message and relevant flights
        """
        today = dt.now()
        flights = Flight.query.filter(
            Flight.departure >= today).all()

        schema = FlightSchema(many=True)

        return return_value(status="success",
                            message=success_messages[
                                'retrieved'].format('Flight'),
                            data=schema.dump(flights).data)


@api.route('/flights/<string:flight_id>')
class SingleFlightResource(Resource):
    """Resource for single flight"""

    def get(self, flight_id):
        """
        Get a single flight record from the database
        :param flight_id: the id of the flight to get
        :return: status, success message, relevant flight
        """
        flight = Flight.get_or_404(flight_id)

        schema = FlightSchema()

        return return_value(data=schema.dump(flight).data,
                            message=success_messages[
                                'retrieved'].format('Flight'),
                            status="success")
