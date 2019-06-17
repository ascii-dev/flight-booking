"""Module to test get all flight endpoint"""
from flask import json
from api.utilities.constants import CHARSET
from api.utilities.messages.success import success_messages

from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL


class TestGetTicketsEndpoints:
    """Class that holds tests for endpoint for getting all tickets"""

    def test_get_all_tickets_succeeds(
            self, init_db, request_header, client, new_ticket):
        """
        Should return a 200 success status message with ticket
        data when all ticket data is gotten
        :param init_db: fixture to initialize the db
        :param request_header: fixture to set request auth header
        :param client: fixture to get flask test client
        :param new_ticket: fixture to get a new ticket
        :return: assertions
        """
        new_ticket.save()
        response = client.get(
            f'{BASE_URL}/tickets',
            headers=request_header)
        response_json = json.loads(response.data.decode(CHARSET))
        tickets = response_json['data']

        assert response.status_code == 200
        assert type(tickets) == list
        assert type(tickets[0]) == dict
        assert response_json['message'] == \
            success_messages['retrieved'].format('Ticket')
        assert "flight" in tickets[0]
        assert "airplane" in tickets[0]["flight"]
        assert "user" in tickets[0]
