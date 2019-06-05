"""Module to test user POST endpoints"""
from flask import json
from api.utilities.constants import CHARSET
from api.utilities.messages.success import success_messages
from api.utilities.messages.serialization import serialization_messages
from tests.mocks.user import VALID_USER_DETAILS, INVALID_USER

from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL


class TestUserPostEndpoints:
    """Test endpoints for creating a new user"""

    def test_create_user_with_valid_data_succeeds(
            self, init_db, client, request_header):
        """
        Should return a 201 status code with new user data and
        token when data provided in request is valid
        :param init_db: fixture to initialize the db
        :param client: fixture to get flask test client
        :param request_header: fixture to add header data to request
        :return: assertions
        """
        response = client.post(
            f'{BASE_URL}/users',
            data=json.dumps(VALID_USER_DETAILS),
            headers=request_header)
        response_json = json.loads(response.data.decode(CHARSET))
        user = response_json['data']['user']

        assert response.status_code == 201
        assert response_json['message'] == success_messages[
            'created'].format('User')
        assert user['firstName'] == VALID_USER_DETAILS['firstName']
        assert user['lastName'] == VALID_USER_DETAILS['lastName']
        assert user['email'] == VALID_USER_DETAILS['email']
        assert 'password' not in user
        assert 'id' in user
        assert type(user['id']) == str
        assert 'token' in response_json['data']
        assert type(response_json['data']['token']) == str

    def test_create_user_with_no_email_fails(
            self, init_db, client, request_header):
        """
        Should return a 400 error code with an error message
        if the user details supplied is missing a valid email
        :param init_db: fixture to initialize the db
        :param client: fixture to get flask test client
        :param request_header: fixture to add header data to request
        :return: assertions
        """
        no_email = INVALID_USER.copy()
        response = client.post(
            f'{BASE_URL}/users',
            data=json.dumps(no_email),
            headers=request_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['email'][0] == \
            serialization_messages['field_required']

    def test_create_user_with_no_password_fails(
            self, init_db, client, request_header):
        """
        Should return a 400 error code with an error message
        if the user details supplied is missing a password
        :param init_db: fixture to initialize the db
        :param client: fixture to get a flask test client
        :param request_header: fixture to add header data to request
        :return: assertions
        """
        no_password = INVALID_USER.copy()
        del no_password['password']
        no_password['email'] = 'spacecraft@asciidev.com.ng'
        response = client.post(
            f'{BASE_URL}/users',
            data=json.dumps(no_password),
            headers=request_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['password'][0] == \
            serialization_messages['field_required']

    def test_create_user_with_already_existing_email_fails(
            self, init_db, client, request_header, new_user):
        """
        Should return a 409 error code with an error message
        if the user's email already exists in the database
        :param init_db: fixture to initialize the db
        :param client: fixture to get a flask test client
        :param new_user: fixture to create a new user
        :param request_header: fixture to add header data to request
        :return: assertions
        """
        new_user.save()
        existing_email = INVALID_USER.copy()
        existing_email['email'] = new_user.email
        response = client.post(
            f'{BASE_URL}/users',
            data=json.dumps(existing_email),
            headers=request_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 409
        assert response_json['status'] == 'error'
        assert response_json['message'] == \
            serialization_messages['exists'].format('User')

    def test_create_user_with_no_first_and_last_name_fails(
            self, init_db, client, request_header):
        """
        Should return a 400 error code with an error message
        if the user details supplied has no first or last name
        :param init_db: fixture to initialize the db
        :param client: fixture to get a flask test client
        :param request_header: fixture to add header data to request
        :return: assertions
        """
        no_first_last_name = INVALID_USER.copy()
        del no_first_last_name['firstName']
        del no_first_last_name['lastName']
        no_first_last_name['email'] = 'somespaceship@asciidev.com.ng'
        response = client.post(
            f'{BASE_URL}/users',
            data=json.dumps(no_first_last_name),
            headers=request_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['firstName'][0] == \
            serialization_messages['field_required']
        assert response_json['errors']['lastName'][0] == \
            serialization_messages['field_required']

    def test_create_user_with_invalid_content_type_fails(
            self, init_db, invalid_header, client):
        """
        Should return a 400 error code with an error message
        if the user creates with an invalid content type
        :param init_db: fixture to initialize the db
        :param invalid_header: fixture for invalid request header
        :param client: fixture to get a flask client
        :return: assertions
        """
        response = client.post(
            f'{BASE_URL}/users',
            data=json.dumps(VALID_USER_DETAILS),
            headers=invalid_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['message'] == \
            serialization_messages['json_type_required']

    def test_create_user_with_invalid_email_structure_fails(
            self, init_db, request_header, client):
        """
        Should return a 400 error code with an error message if the
        user creates with an invalid email structure
        :param init_db: fixture to initialize the db
        :param request_header: fixture for invalid request header
        :param client: fixture to get a flask client
        :return: assertions
        """
        invalid_email = INVALID_USER.copy()
        invalid_email['email'] = 'someremail.gmail.com'
        response = client.post(
            f'{BASE_URL}/users',
            data=json.dumps(invalid_email),
            headers=request_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['errors']['email'][0] == \
            serialization_messages['invalid_email']

    def test_create_user_with_invalid_first_and_last_name_fails(
            self, init_db, request_header, client):
        """
        Should return a 400 error code with an error message if the
        user creates with an invalid first name and last name
        :param init_db: fixture to initialize the db
        :param request_header: fixture for invalid request header
        :param client: fixture to get a flask client
        :return: assertions
        """
        invalid_email = INVALID_USER.copy()
        invalid_email['firstName'] = '!@#$%^&*()...'
        invalid_email['lastName'] = '!@#$%^&*()...'
        response = client.post(
            f'{BASE_URL}/users',
            data=json.dumps(invalid_email),
            headers=request_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['errors']['firstName'][0] == \
            serialization_messages['string_characters']
        assert response_json['errors']['lastName'][0] == \
            serialization_messages['string_characters']

    def test_create_user_with_empty_first_and_last_name_fails(
            self, init_db, request_header, client):
        """
        Should return a 400 error code with an error message if the
        user creates with first name and last name as empty strings
        :param init_db: fixture to initialize the db
        :param request_header: fixture for invalid request header
        :param client: fixture to get a flask client
        :return: assertions
        """
        invalid_email = INVALID_USER.copy()
        invalid_email['firstName'] = ''
        invalid_email['lastName'] = ''
        response = client.post(
            f'{BASE_URL}/users',
            data=json.dumps(invalid_email),
            headers=request_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['errors']['firstName'][0] == \
            serialization_messages['not_empty']
        assert response_json['errors']['lastName'][0] == \
            serialization_messages['not_empty']

    def test_create_user_first_last_name_grater_than_60_characters_fails(
            self, init_db, request_header, client):
        """
        Should return a 400 error code with an error message if the
        user creates with first name and last name longer than 60 characters
        :param init_db: fixture to initialize the db
        :param request_header: fixture for invalid request header
        :param client: fixture to get a flask client
        :return: assertions
        """
        invalid_email = INVALID_USER.copy()
        string_with_65_characters = 'asdf' * 60
        invalid_email['firstName'] = string_with_65_characters
        invalid_email['lastName'] = string_with_65_characters
        response = client.post(
            f'{BASE_URL}/users',
            data=json.dumps(invalid_email),
            headers=request_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['errors']['firstName'][0] == \
            serialization_messages['string_length']
        assert response_json['errors']['lastName'][0] == \
            serialization_messages['string_length']

    def test_create_user_with_password_less_than_five_characters_fails(
            self, init_db, request_header, client):
        """
        Should return a 400 error code with an error message if the
        user creates with a password less than five characters
        :param init_db: fixture to initialize the db
        :param request_header: fixture for invalid request header
        :param client: fixture to get a flask client
        :return: assertions
        """
        invalid_email = INVALID_USER.copy()
        invalid_email['password'] = 'as'
        response = client.post(
            f'{BASE_URL}/users',
            data=json.dumps(invalid_email),
            headers=request_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['errors']['password'][0] == \
            serialization_messages['field_length'].format(5)
