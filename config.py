import sys
from os import getenv
from pathlib import Path

from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)


class Config:
    """App base configuration"""

    DEBUG = False
    TESTING = False
    FLASK_ENV = getenv('FLASK_ENV', 'production')
    PORT = getenv('PORT', 5000)
    SWAGGER_URL = '/'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = getenv(
        'DATABASE_URI',
        'postgresql://localhost/flight_booking')
    JWT_SECRET_KEY = getenv('JWT_SECRET_KEY_STAGING')
    CELERY_BROKER_URL = getenv(
        'CELERY_BROKER_URL_STAGING', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = getenv(
        'CELERY_RESULT_BACKEND_STAGING', 'redis://localhost:6379/0')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = getenv('MAIL_DEFAULT_SENDER')
    MAIL_USERNAME = getenv('MAIL_USERNAME')
    MAIL_PORT = 587
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_USE_TLS = True
    CLOUDINARY_CLOUD_NAME = getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = getenv('CLOUDINARY_API_SECRET')


class StagingConfig(Config):
    """App staging configuration"""

    pass


class ProductionConfig(Config):
    """App production configuration"""

    JWT_SECRET_KEY = getenv('JWT_SECRET_KEY_PRODUCTION')
    CELERY_BROKER_URL = getenv(
        'CELERY_BROKER_URL_PRODUCTION', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = getenv(
        'CELERY_RESULT_BACKEND_PRODUCTION', 'redis://localhost:6379/0')


class DevelopmentConfig(Config):
    """App development configuration"""

    DEBUG = True


class TestingConfig(Config):
    """App testing configuration"""

    DEBUG = True
    TESTING = True
    FLASK_ENV = 'testing'
    SQLALCHEMY_DATABASE_URI = getenv(
        'TEST_DATABASE_URI',
        'postgresql://localhost/flight_booking_test')
    API_BASE_URL = getenv('API_BASE_URL', '/api/v1')
    JWT_SECRET_KEY = getenv('JWT_SECRET_KEY_TEST')


config = {
    "staging": StagingConfig,
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
}

AppConfig = TestingConfig if 'pytest' in sys.modules else config.get(
    getenv('FLASK_ENV'), 'development')

