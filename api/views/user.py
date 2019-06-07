"""Module that holds users endpoints"""
from flask import request
from flask_restplus import Resource
from werkzeug.security import check_password_hash

from main import api

from ..models.user import User
from ..utilities.messages.success import success_messages
from ..utilities.helpers.generate_token import generate_token
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

        token = generate_token(user)

        return {
            "status": "success",
            "message": success_messages['created'].format('User'),
            "data": {
                "token": token,
                "user": schema.dump(user).data,
            },
        }, 201


@api.route('/users/login')
class LoginResource(Resource):
    """Resource for user login"""

    @validate_json_request
    def post(self):
        """
        Create a new user record in the database
        :return: status, success message and relevant user details
        """
        request_data = request.get_json()

        user = User.query.filter_by(email=request_data['email']).first()
        if not user or not check_password_hash(
                user.password, request_data['password']):
            raise ValidationError({
                'message': serialization_messages['not_found'].format('User')
            }, 400)

        token = generate_token(user)
        schema = UserSchema()

        return {
            "message": success_messages['retrieved'].format('User'),
            "data": {
                "token": token,
                "user": schema.dump(user).data
            },
            "status": "success"
        }, 200
