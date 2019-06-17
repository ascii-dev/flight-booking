"""Module to test new ticket endpoint"""
from flask import json
from api.utilities.constants import CHARSET
from api.utilities.messages.error import error_messages
from api.utilities.messages.success import success_messages


from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL


class TestTicketCreationEndpoints:
    """Class that holds tests for new ticket endpoint"""

    def test_admin_create_new_ticket_valid_data_succeeds(
            self, init_db, user_auth_header, client, new_flight):
        """
        Should return a 201 created status message with ticket
        data if an admin creates a ticket with valid data
        :param init_db: fixture to initialize the db
        :param user_auth_header: fixture to set request auth header
        :param client: fixture to get flask test client
        :param new_flight: fixture to get a new flight
        :return: assertions
        """
        new_flight.save()
        response = client.post(
            f'{BASE_URL}/flights/{new_flight.id}/book',
            headers=user_auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        ticket = response_json['data']
        flight = ticket['flight']
        airplane = flight['airplane']
        user = ticket['user']
        header_user = user_auth_header['User']

        assert response.status_code == 201
        assert response_json['message'] == \
            success_messages['created'].format('Ticket')
        assert ticket['status'] == 'pending'
        assert flight['id'] == new_flight.id
        assert flight['from'] == new_flight.flying_from
        assert flight['to'] == new_flight.flying_to
        assert airplane['capacity'] == new_flight.airplane.capacity
        assert airplane['id'] == new_flight.airplane.id
        assert airplane['model'] == new_flight.airplane.model
        assert airplane['brand'] == new_flight.airplane.brand
        assert user['id'] == header_user.id
        assert user['firstName'] == header_user.first_name
        assert user['lastName'] == header_user.last_name
        assert user['email'] == header_user.email

    def test_user_create_new_ticket_when_capacity_is_full_fails(
            self, init_db, user_auth_header, client, new_flight):
        """
        Should return a 401 error status with error message
        if a user tries to create an ticket airplane when capacity
        is full
        :param init_db: fixture to initialize the db
        :param user_auth_header: fixture to set request auth header
        :param client: fixture to get flask test client
        :param new_flight: fixture to get a new flight
        :return: assertions
        """
        new_flight.save()
        new_flight.airplane.capacity = 0
        response = client.post(
            f'{BASE_URL}/flights/{new_flight.id}/book',
            headers=user_auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 412
        assert response_json['status'] == 'error'
        assert response_json['message'] == \
            error_messages['full'].format('Flight')

    def test_user_create_new_ticket_invalid_flight_id_fails(
            self, init_db, user_auth_header, client):
        """
        Should return a 400 error status with error message
        if a user tries to create an ticket airplane when capacity
        is full
        :param init_db: fixture to initialize the db
        :param user_auth_header: fixture to set request auth header
        :param client: fixture to get flask test client
        :return: assertions
        """
        response = client.post(
            f'{BASE_URL}/flights/-Lg7TAnsRBs6Em_C8ZkI/book',
            headers=user_auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == \
            error_messages['not_found'].format('Flight')
