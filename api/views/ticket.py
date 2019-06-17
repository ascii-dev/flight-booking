"""Module that holds tickets endpoints"""
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import Resource

from api.utilities.helpers.return_value import return_value
from api.utilities.messages.error import error_messages
from api.utilities.validators.base_validator import ValidationError
from main import api

from ..models.flight import Flight
from ..models.ticket import Ticket

from ..utilities.messages.success import success_messages
from ..utilities.validators.validate_json_request import validate_json_request

from ..schemas.ticket import TicketSchema


@api.route('/flights/<string:flight_id>/book')
class TicketsResource(Resource):
    """Resource for ticket creation"""

    @jwt_required
    @validate_json_request
    def post(self, flight_id):
        """
        Create a new ticket record in the database
        :return: status, success message and relevant ticket details
        """
        flight = Flight.get_or_404(flight_id)

        user = get_jwt_identity()
        request_data = {
            'flight_id': flight.id,
            'user_id': user['id']
        }

        all_flight_tickets = Ticket.query.filter_by(
            flight_id=flight_id).count()
        if all_flight_tickets >= flight.airplane.capacity:
            raise ValidationError({
                "message": error_messages['full'].format('Flight')
            }, 412)

        schema = TicketSchema()
        ticket_data = schema.load_object_into_schema(request_data)

        ticket = Ticket(**ticket_data)
        ticket.save()

        return return_value(data=schema.dump(ticket).data,
                            message=success_messages[
                                'created'].format('Ticket'),
                            status="success",
                            status_code=201)
