import pytest
from datetime import datetime as dt, timedelta
from api.models import Flight


@pytest.fixture(scope='module')
def new_flight(app, new_airplane):
    """
    Fixture to create a new flight
    :param app: app instance
    :return: a new flight instance
    """
    new_airplane.save()
    tomorrow = dt.now() + timedelta(1)
    params = {
        'airplane_id': new_airplane.id,
        'flying_from': 'Lagos, Nigeria',
        'flying_to': 'San Francisco, United States',
        'departure': tomorrow.strftime("%Y-%m-%d %H:%M:%S"),
        'arrival': tomorrow.strftime("%Y-%m-%d %H:%M:%S"),
    }
    return Flight(**params)


@pytest.fixture(scope='module')
def new_flight_no_capacity(app, new_airplane):
    pass
