import pytest

from api.utilities.constants import MIMETYPE, INVALID_MIMETYPE


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
