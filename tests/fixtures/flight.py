import pytest
from datetime import datetime as dt
from api.models import Flight


@pytest.fixture(scope='module')
def new_flight(app, new_airplane):
    """
    Fixture to create a new flight
    :param app: app instance
    :return: a new flight instance
    """
    new_airplane.save()
    params = {
        'airplane_id': new_airplane.id,
        'flying_from': 'Lagos, Nigeria',
        'flying_to': 'San Francisco, United States',
        'departure': dt.now(),
        'arrival': dt.now(),
    }
    return Flight(**params)
