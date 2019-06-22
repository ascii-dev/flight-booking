import pytest

from faker import Faker

from api.models import User

fake = Faker()


@pytest.fixture(scope='module')
def new_user(app, init_db):
    """
    Fixture to create a new user
    :param app: app instance
    :param init_db: fixture to initialize the db
    :return: a new user instance
    """
    print(fake.name())
    params = {
        'first_name': 'Samuel',
        'last_name': 'Afolaranmi',
        'email': 'somerandomemail@asciidev.com.ng',
        'password': 'somesecretpassword',
        'passport_photograph': {
            'public_id': fake.name()
        }
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
        'role': 'admin',
        'passport_photograph': {
            'public_id': fake.name()
        }
    }
    return User(**params)
