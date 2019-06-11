import pytest

from api.models import User


@pytest.fixture(scope='module')
def new_user(app, init_db):
    """
    Fixture to create a new user
    :param app: app instance
    :param init_db: fixture to initialize the db
    :return: a new user instance
    """
    params = {
        'first_name': 'Samuel',
        'last_name': 'Afolaranmi',
        'email': 'somerandomemail@asciidev.com.ng',
        'password': 'somesecretpassword',
    }
    return User(**params)


@pytest.fixture(scope='module')
def new_admin(app, init_db):
    """
    Fixture to create a new admin
    :param app: app instance
    :param init_db: fixture to initialize the db
    :return: a new admin instance
    """
    params = {
        'first_name': 'Shola',
        'last_name': 'Spacer',
        'email': 'sholaspacer@asciidev.com.ng',
        'password': 'supersecretpassword',
        'role': 'admin'
    }
    return User(**params)
