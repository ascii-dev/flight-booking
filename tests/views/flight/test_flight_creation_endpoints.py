"""Module to test new flight endpoint"""
from flask import json
from api.utilities.constants import CHARSET
from api.utilities.messages.error import error_messages
from api.utilities.messages.success import success_messages
from api.utilities.messages.serialization import serialization_messages

from tests.mocks.flight import VALID_FLIGHT_DATA, INVALID_FLIGHT_DATA

from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL


class TestFlightCreationEndpoints:
    """Class that holds tests for new flight endpoint"""

    def test_admin_create_new_flight_valid_data_succeeds(
            self, init_db, admin_auth_header, client, new_airplane):
        """
        Should return a 201 created status message with flight
        data if an admin creates a flight with valid data
        :param init_db: fixture to initialize the db
        :param admin_auth_header: fixture to set request auth header
        :param client: fixture to get flask test client
        :param new_airplane: fixture to get a new airplane
        :return: assertions
        """
        new_airplane.save()
        response = client.post(
            f'{BASE_URL}/airplanes/{new_airplane.id}/flights',
            data=json.dumps(VALID_FLIGHT_DATA),
            headers=admin_auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        flight = response_json['data']
        airplane = flight['airplane']

        assert response.status_code == 201
        assert response_json['message'] == \
            success_messages['created'].format('Flight')
        assert type(flight) == dict
        assert type(airplane) == dict
        assert 'id' in flight and type(flight['id']) == str
        assert 'from' in flight and type(flight['from']) == str
        assert 'to' in flight and type(flight['to']) == str
        assert 'departure' in flight and type(flight['departure']) == str
        assert 'arrival' in flight and type(flight['arrival']) == str
        assert 'id' in airplane and type(airplane['id']) == str
        assert 'model' in airplane and type(airplane['model']) == str
        assert 'brand' in airplane and type(airplane['brand']) == str
        assert 'capacity' in airplane and type(airplane['capacity']) == int

    def test_admin_create_new_flight_invalid_data_fails(
            self, init_db, admin_auth_header, client, new_airplane):
        """
        Should return a 400 error status with error messages
        if an admin creates a flight with invalid data
        :param init_db: fixture to initialize the db
        :param admin_auth_header: fixture to set request auth header
        :param client: fixture to get flask test client
        :param new_airplane: fixture to get a new airplane
        :return: assertions
        """
        new_airplane.save()
        response = client.post(
            f'{BASE_URL}/airplanes/{new_airplane.id}/flights',
            data=json.dumps(INVALID_FLIGHT_DATA),
            headers=admin_auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['from'][0] == \
            serialization_messages['not_empty']
        assert response_json['errors']['to'][0] == \
            serialization_messages['not_empty']
        assert response_json['errors']['departure'][0] == \
            serialization_messages['invalid_datetime']
        assert response_json['errors']['arrival'][0] == \
            serialization_messages['invalid_datetime']

    def test_user_create_new_flight_valid_data_fails(
            self, init_db, user_auth_header, client, new_airplane):
        """
        Should return a 400 error status with error message
        if a user tries to create an airplane with valid data
        :param init_db: fixture to initialize the db
        :param user_auth_header: fixture to set request auth header
        :param client: fixture to get flask test client
        :param new_airplane: fixture to get a new airplane
        :return: assertions
        """
        new_airplane.save()
        flight = VALID_FLIGHT_DATA.copy()
        flight['from'] = 'Heathrow, London, UK'
        response = client.post(
            f'{BASE_URL}/airplanes/{new_airplane.id}/flights',
            data=json.dumps(flight),
            headers=user_auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == \
            error_messages['not_allowed']
