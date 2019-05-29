import pytest

from api.models import Airplane


@pytest.fixture(scope='module')
def new_airplane(app):
    """
    Fixture to create a new airplane
    :param app: app instance
    :return: a new airplane instance
    """
    params = {
        'brand': 'Dujoko',
        'model': 'DJK45OH',
        'capacity': 145
    }
    return Airplane(**params)
