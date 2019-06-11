import pytest

from api.utilities.constants import MIMETYPE, INVALID_MIMETYPE
from tests.generate_test_token import generate_test_token


@pytest.fixture(scope='module')
def request_header():
    return {
        'Content-Type': MIMETYPE,
        'Accept': MIMETYPE
    }


@pytest.fixture(scope='module')
def invalid_header():
    return {
        'Content-Type': INVALID_MIMETYPE,
        'Accept': INVALID_MIMETYPE
    }


@pytest.fixture(scope='module')
def admin_auth_header(new_admin):
    admin = new_admin.save()
    return {
        'Authorization': f'Bearer {generate_test_token(admin)}',
        'Content-Type': MIMETYPE,
        'Accept': MIMETYPE
    }


@pytest.fixture(scope='module')
def user_auth_header(new_user):
    user = new_user.save()
    return {
        'Authorization': f'Bearer {generate_test_token(user)}',
        'Content-Type': MIMETYPE,
        'Accept': MIMETYPE
    }
