"""Module to test user POST endpoints"""
from flask import json
from api.utilities.constants import CHARSET
from api.utilities.messages.success import success_messages
from api.utilities.messages.serialization import serialization_messages

from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL


class TestUserLoginEndpoints:
    """Test endpoints to log a user in"""

    def test_user_login_with_valid_credentials_succeeds(
            self, init_db, new_user, request_header, client):
        """
        Should return a 200 status code with a user details if a
        user logs in with valid details
        :param init_db: fixture to initialize the db
        :param new_user: fixture to create a new user
        :param request_header: fixture to set request header
        :param client: fixture to get a flask test client
        :return: assertions
        """
        # import pdb; pdb.set_trace()
        password = new_user.password
        new_user.save()
        login_data = {
            'email': new_user.email,
            'password': password,
        }
        response = client.post(
            f'{BASE_URL}/users/login',
            data=json.dumps(login_data),
            headers=request_header)
        response_json = json.loads(response.data.decode(CHARSET))
        user = response_json['data']['user']

        assert response.status_code == 200
        assert response_json['message'] == success_messages[
            'retrieved'].format('User')
        assert user['firstName'] == new_user.first_name
        assert user['lastName'] == new_user.last_name
        assert user['email'] == new_user.email
        assert 'password' not in user
        assert 'id' in user
        assert type(user['id']) == str
        assert 'token' in response_json['data']
        assert type(response_json['data']['token']) == str

    def test_user_login_with_incorrect_password_fails(
            self, init_db, new_user, request_header, client):
        """
        Should return a 400 error status code and an error message
        if a user logs in with an incorrect password
        :param init_db: fixture to initialize the db
        :param new_user: fixture to get a new user
        :param request_header: fixture to set request header
        :param client: fixture to get a flask test client
        :return: assertions
        """
        new_user.save()
        login_data = {
            "email": new_user.email,
            "password": "!@#$%%^&*(",
        }
        response = client.post(
            f'{BASE_URL}/users/login',
            data=json.dumps(login_data),
            headers=request_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['message'] == \
            serialization_messages['not_found'].format('User')

    def test_user_login_with_incorrect_email_fails(
            self, init_db, new_user, request_header, client):
        """
        Should return a 400 error status code and an error message
        if a user logs in with an incorrect email
        :param init_db: fixture to initialize the db
        :param new_user: fixture to get a new user
        :param request_header: fixture to set request header
        :param client: fixture to get a flask test client
        :return: assertions
        """
        new_user.save()
        login_data = {
            "email": "doremi@asciidev.com.ng",
            "password": new_user.password,
        }
        response = client.post(
            f'{BASE_URL}/users/login',
            data=json.dumps(login_data),
            headers=request_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['message'] == \
            serialization_messages['not_found'].format('User')
