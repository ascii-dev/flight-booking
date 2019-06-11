"""Module that holds airplane endpoints"""
from flask import request
from flask_jwt_extended import jwt_required
from flask_restplus import Resource

from main import api

from ..models.airplane import Airplane
from ..utilities.messages.success import success_messages
from ..utilities.validators.base_validator import ValidationError
from ..utilities.messages.serialization import serialization_messages
from ..utilities.validators.validate_json_request import validate_json_request
from ..utilities.validators.validate_admin_access import validate_admin_access
from ..schemas.airplane import AirplaneSchema


@api.route('/airplanes')
class AirplanesResource(Resource):
    """Resource for airplane creation and multiple airplane data"""

    @jwt_required
    @validate_json_request
    @validate_admin_access
    def post(self):
        """
        Create a new airplane record in the database
        :return: status, success message and relevant airplane details
        """
        request_data = request.get_json()

        existing_airplane = Airplane.query.filter_by(**request_data).first()
        if existing_airplane:
            raise ValidationError({
                "message": serialization_messages['exists'].format('Airplane')
            }, 409)

        schema = AirplaneSchema()
        airplane_data = schema.load_object_into_schema(request_data)
        airplane = Airplane(**airplane_data)
        airplane.save()

        return {
            "status": "success",
            "message": success_messages['created'].format('Airplane'),
            "data": schema.dump(airplane).data,
        }, 201
