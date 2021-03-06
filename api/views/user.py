"""Module that holds users endpoints"""
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restplus import Resource
from werkzeug.security import check_password_hash
import cloudinary
import cloudinary.uploader

from main import api
from config import AppConfig

from celery_conf.tasks import delete_passport

from ..models.user import User
from ..utilities.helpers.return_value import return_value
from ..utilities.messages.success import success_messages
from ..utilities.helpers.generate_token import generate_token
from ..utilities.validators.base_validator import ValidationError
from ..utilities.messages.serialization import serialization_messages
from ..utilities.validators.validate_json_request import validate_json_request
from ..utilities.helpers.adapt_resource_to_env import adapt_resource_to_env
from ..schemas.user import UserSchema


cloudinary.config.update = ({
    'cloud_name': AppConfig.CLOUDINARY_CLOUD_NAME,
    'api_key': AppConfig.CLOUDINARY_API_KEY,
    'api_secret': AppConfig.CLOUDINARY_API_SECRET
})


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
        data = {
            "token": token,
            "user": schema.dump(user).data,
        }

        return return_value(status="success",
                            message=success_messages[
                                'created'].format('User'),
                            data=data,
                            status_code=201)


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

        data = {
            "token": token,
            "user": schema.dump(user).data,
        }

        return return_value(status="success",
                            message=success_messages[
                                'retrieved'].format('User'),
                            data=data)


@api.route('/users/passport')
class PassportResource(Resource):
    """Resource for user login"""

    # @staticmethod
    # def upload_to_cloudinary(file):
    #     return cloudinary.uploader.upload(file)
    #
    # @staticmethod
    # def delete_cloudinary(self, public_id):
    #     delete_from_cloudinary = adapt_resource_to_env(
    #         delete_passport.delay)
    #     delete_from_cloudinary(public_id)

    @jwt_required
    def post(self):
        """
        Uploads passport photograph for a user
        :return: status, success message and relevant user details
        """
        user = User.get_or_404(get_jwt_identity()['id'])
        user.update(
            passport_photograph=cloudinary.uploader.upload(
                request.files['passport']))

        schema = UserSchema()
        user = schema.dump(user).data

        return return_value(data=user,
                            status="success",
                            message=success_messages[
                                'created'].format('Passport'),
                            status_code=201)

    @jwt_required
    def delete(self):
        """
        Deletes a user's passport photograph both locally and
        on cloudinary
        :return: status, success message
        """
        user = User.get_or_404(get_jwt_identity()['id'])

        delete_from_cloudinary = adapt_resource_to_env(
            delete_passport.delay)
        delete_from_cloudinary(user.passport_photograph['public_id'])

        user.update(passport_photograph=None)

        return return_value(status="success",
                            message=success_messages[
                                'deleted'].format('Passport'))

    @jwt_required
    def patch(self):
        """
        Updates a user's passport photograph both locally and
        on cloudinary
        :return: status, success message
        """
        user = User.get_or_404(get_jwt_identity()['id'])

        delete_from_cloudinary = adapt_resource_to_env(
            delete_passport.delay)
        delete_from_cloudinary(user.passport_photograph['public_id'])

        user.update(passport_photograph=cloudinary.uploader.upload(
                request.files['passport']))
        user = UserSchema().dump(user).data

        return return_value(status="success",
                            data=user,
                            message=success_messages[
                                'updated'].format('Passport'))
