import json
import os
from unittest import mock

import cloudinary
import cloudinary.uploader

from api.utilities.constants import CHARSET
from api.utilities.messages.success import success_messages
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL


class TestPassportDeletionEndpoint:
    """Class to hold tests for passport deletion endpoint"""
    def test_user_deletes_image_successfully(
            self, client, user_auth_header, init_db):
        """
        Tests that a user can upload image successfully
        :param client: fixture to get flask test client
        :param user_auth_header: fixture to set authentication header
        :param init_db: fixture to initialize the db
        :return: assertions
        """
        cloudinary.api.delete_resources = mock.Mock()
        cloudinary.uploader.upload = mock.Mock(
            return_value={'url': 'someimage'})
        asset = "6e609595.jpeg"
        passport = os.path.join(
            os.path.dirname(__file__), f"../../../templates/assets/{asset}")
        response = client.patch(
            f'{BASE_URL}/users/passport',
            headers=user_auth_header,
            content_type='multipart/form-data',
            data={
                "passport": (passport, asset)
            })

        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['data']

        assert response.status_code == 200
        assert response_json['message'] == success_messages[
            'updated'].format('Passport')
        assert 'passport' in response_data
