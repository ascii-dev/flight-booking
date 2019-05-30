import pytest

from api.models import Ticket


@pytest.fixture(scope='module')
def new_ticket(app, new_user, new_flight):
    """
    Fixture to create a new flight
    :param app: app instance
    :param new_user: a fixture to create a new user
    :param new_flight: a fixture to create a new flight
    :return: a new ticket instance
    """
    new_user.save()
    new_flight.save()
    params = {
        'user_id': new_user.id,
        'flight_id': new_flight.id,
        'status': 'pending'
    }
    return Ticket(**params)
