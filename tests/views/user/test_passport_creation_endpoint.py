import json
import os
from unittest import mock

from api.utilities.constants import CHARSET
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL


class TestPassportCreationEndpoint:
    """Class to hold tests for passport creation endpoint"""
    def test_user_uploads_image_successfully(
            self, client, user_auth_header, init_db):
        """
        Tests that a user can upload image successfully
        :param client: fixture tto get flask test client
        :param user_auth_header: fixture to set authentication header
        :param init_db: fixture to initialize the db
        :return: assertions
        """
        import cloudinary.uploader
        cloudinary.uploader.upload = mock.Mock(
            return_value={'url': 'someimage'})
        asset = "6e609595.jpeg"
        passport = os.path.join(os.path.dirname(__file__), f"./assets/{asset}")
        response = client.post(
            f'{BASE_URL}/users/passport',
            headers=user_auth_header,
            content_type='multipart/form-data',
            data={
                "passport": (passport, asset)
            })

        response_json = json.loads(response.data.decode(CHARSET))['data']
        passport = response_json['passport']

        assert response.status_code == 201
        assert 'passport' in response_json
        assert type(passport).__name__ == 'dict'
