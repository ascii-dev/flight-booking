"""Module to test get a single flight endpoint"""
from flask import json
from api.utilities.constants import CHARSET
from api.utilities.messages.serialization import serialization_messages
from api.utilities.messages.success import success_messages

from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL


class TestFlightCreationEndpoints:
    """Class that holds tests for endpoint for getting a single flight"""

    def test_get_single_flight_valid_id_succeeds(
            self, init_db, request_header, client, new_flight):
        """
        Should return a 200 success status message with flight
        data when a single flight data is gotten
        :param init_db: fixture to initialize the db
        :param request_header: fixture to set request auth header
        :param client: fixture to get flask test client
        :param new_flight: fixture to get a new flight
        :return: assertions
        """
        new_flight.save()
        response = client.get(
            f'{BASE_URL}/flights/{new_flight.id}',
            headers=request_header)
        response_json = json.loads(response.data.decode(CHARSET))
        flight = response_json['data']

        assert response.status_code == 200
        assert response_json['message'] == \
            success_messages['retrieved'].format('Flight')
        assert type(flight) == dict
        assert 'id' in flight and type(flight['id']) == str
        assert 'from' in flight and type(flight['from']) == str
        assert 'to' in flight and type(flight['to']) == str
        assert 'departure' in flight and \
               type(flight['departure']) == str
        assert 'arrival' in flight and \
               type(flight['arrival']) == str
        assert 'id' in flight['airplane'] and \
               type(flight['airplane']['id']) == str
        assert 'model' in flight['airplane'] and \
               type(flight['airplane']['model']) == str
        assert 'brand' in flight['airplane'] and \
               type(flight['airplane']['brand']) == str
        assert 'capacity' in flight['airplane'] and \
               type(flight['airplane']['capacity']) == int

    def test_get_single_flight_invalid_id_fails(
            self, init_db, request_header, client):
        """
        Should return a 200 success status message with flight
        data when all flight data is gotten
        :param init_db: fixture to initialize the db
        :param request_header: fixture to set request auth header
        :param client: fixture to get flask test client
        :return: assertions
        """
        response = client.get(
            f'{BASE_URL}/flights/-Lg7TAm5PQfqBFoSakTa',
            headers=request_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['message'] == \
            serialization_messages['not_found'].format('Flight')
