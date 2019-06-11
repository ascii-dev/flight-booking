"""Module to test new airplane endpoint"""
from flask import json
from api.utilities.constants import CHARSET
from api.utilities.messages.error import error_messages
from api.utilities.messages.success import success_messages
from api.utilities.messages.serialization import serialization_messages

from tests.mocks.airplane import VALID_AIRPLANE_DATA, INVALID_AIRPLANE_DATA

from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL


class TestNewAirplaneEndpoint:
    """Class that holds tests for new airplane endpoint"""

    def test_admin_create_new_airplane_valid_data_succeeds(
            self, init_db, admin_auth_header, client):
        """
        Should return a 201 created status message with airplane
        data if an admin creates an airplane with valid data
        :param init_db: fixture to initialize the db
        :param admin_auth_header: fixture to set request auth header
        :param client: fixture to get flask test client
        :return: assertions
        """
        response = client.post(
            f'{BASE_URL}/airplanes',
            data=json.dumps(VALID_AIRPLANE_DATA),
            headers=admin_auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        airplane = response_json['data']

        assert response.status_code == 201
        assert response_json['message'] == \
            success_messages['created'].format('Airplane')
        assert type(airplane) == dict
        assert 'id' in airplane and type(airplane['id']) == str
        assert 'model' in airplane and type(airplane['model']) == str
        assert 'brand' in airplane and type(airplane['brand']) == str
        assert 'capacity' in airplane and type(airplane['capacity']) == int

    def test_admin_create_new_airplane_invalid_data_fails(
            self, init_db, admin_auth_header, client):
        """
        Should return a 400 error status with error messages
        if an admin creates an airplane with invalid data
        :param init_db: fixture to initialize the db
        :param admin_auth_header: fixture to set request auth header
        :param client: fixture to get flask test client
        :return: assertions
        """
        response = client.post(
            f'{BASE_URL}/airplanes',
            data=json.dumps(INVALID_AIRPLANE_DATA),
            headers=admin_auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['model'][0] == \
            serialization_messages['not_empty']
        assert response_json['errors']['brand'][0] == \
            serialization_messages['not_empty']
        assert response_json['errors']['capacity'][0] == \
            serialization_messages['field_required']

    def test_user_create_new_airplane_valid_data_fails(
            self, init_db, user_auth_header, client):
        """
        Should return a 400 error status with error message
        if a user tries to create an airplane with valid data
        :param init_db: fixture to initialize the db
        :param user_auth_header: fixture to set request auth header
        :param client: fixture to get flask test client
        :return: assertions
        """
        airplane = VALID_AIRPLANE_DATA.copy()
        airplane['brand'] = 'Super123'
        response = client.post(
            f'{BASE_URL}/airplanes',
            data=json.dumps(airplane),
            headers=user_auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == \
            error_messages['not_allowed']

    def test_admin_create_duplicate_airplane_fails(
            self,
            init_db,
            admin_auth_header,
            client,
            new_airplane):
        """
        Should return a 400 error status with error message if an
        admin tries to create a duplicate airplane
        :param init_db: fixture to initialize the db
        :param admin_auth_header: fixture to set request header
        :param client: fixture to get flask test client
        :param new_airplane: fixture to create a new airplane
        :return: assertions
        """
        new_airplane.save()
        new_data = {
            'model': new_airplane.model,
            'brand': new_airplane.brand,
            'capacity': new_airplane.capacity,
        }
        response = client.post(
            f'{BASE_URL}/airplanes',
            data=json.dumps(new_data),
            headers=admin_auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 409
        assert response_json['status'] == 'error'
        assert response_json['message'] == \
            serialization_messages['exists'].format('Airplane')
