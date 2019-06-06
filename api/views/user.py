"""Module that holds users endpoints"""
from flask import request
from flask_restplus import Resource
from flask_jwt_extended import create_access_token

from main import api

from ..models.user import User
from ..utilities.messages.success import success_messages
from ..utilities.validators.base_validator import ValidationError
from ..utilities.messages.serialization import serialization_messages
from ..utilities.validators.validate_json_request import validate_json_request
from ..schemas.user import UserSchema


@api.route('/users')
class UsersResource(Resource):
    """Resource for user creation and multiple user data"""

    @validate_json_request
    def post(self):
        """
        Create a new user record in the database
        :return: status, success message and relevant user details
        """
        request_data = request.get_json()

        schema = UserSchema()
        user_data = schema.load_object_into_schema(request_data)

        user = User.query.filter_by(email=request_data['email']).first()
        if user:
            raise ValidationError(
                {
                    'message': serialization_messages['exists'].format('User')
                }, 409)

        user = User(**user_data)
        user.save()

        token = create_access_token(identity=dict(
            id=user.id,
            firstName=user.first_name,
            lastName=user.last_name,
            email=user.email,
            role=user.role.value))

        return {
            "status": "success",
            "message": success_messages['created'].format('User'),
            "data": {
                "token": token,
                "user": schema.dump(user).data,
            },
        }, 201
