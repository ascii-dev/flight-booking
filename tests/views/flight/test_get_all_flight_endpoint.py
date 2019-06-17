"""Module to test get all flight endpoint"""
from flask import json
from api.utilities.constants import CHARSET
from api.utilities.messages.success import success_messages

from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL


class TestGetFlightEndpoints:
    """Class that holds tests for endpoint for getting all flights"""

    def test_get_all_flights_succeeds(
            self, init_db, request_header, client, new_flight):
        """
        Should return a 200 success status message with flight
        data when all flight data is gotten
        :param init_db: fixture to initialize the db
        :param request_header: fixture to set request auth header
        :param client: fixture to get flask test client
        :param new_flight: fixture to get a new flight
        :return: assertions
        """
        new_flight.save()
        response = client.get(
            f'{BASE_URL}/flights',
            headers=request_header)
        response_json = json.loads(response.data.decode(CHARSET))
        flights = response_json['data']

        assert response.status_code == 200
        assert response_json['message'] == \
            success_messages['retrieved'].format('Flight')
        assert type(flights) == list
        assert type(flights[0]) == dict
        assert 'id' in flights[0] and type(flights[0]['id']) == str
        assert 'from' in flights[0] and type(flights[0]['from']) == str
        assert 'to' in flights[0] and type(flights[0]['to']) == str
        assert 'departure' in flights[0] and \
               type(flights[0]['departure']) == str
        assert 'arrival' in flights[0] and \
               type(flights[0]['arrival']) == str
        assert 'id' in flights[0]['airplane'] and \
               type(flights[0]['airplane']['id']) == str
        assert 'model' in flights[0]['airplane'] and \
               type(flights[0]['airplane']['model']) == str
        assert 'brand' in flights[0]['airplane'] and \
               type(flights[0]['airplane']['brand']) == str
        assert 'capacity' in flights[0]['airplane'] and \
               type(flights[0]['airplane']['capacity']) == int
