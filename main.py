"""Module for application factory"""

from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_restplus import Api
from flask_jwt_extended import JWTManager
from celery import Celery
from flask_mail import Mail

from config import AppConfig

from api import api_blueprint
from api.utilities.validators.base_validator import middleware_blueprint, \
    ValidationError
from api.models.database import db

api = Api(api_blueprint, doc='/')
celery_app = Celery(__name__, broker=AppConfig.CELERY_BROKER_URL)
mail = Mail()


def initialize_error_handlers(application):
    """Initialize error handlers"""
    application.register_blueprint(middleware_blueprint)
    application.register_blueprint(api_blueprint)


def create_app(config=AppConfig):
    """Return app object given config object"""

    app = Flask(__name__)
    app.config.from_object(config)
    app.url_map.strict_slashes = False
    celery_app.conf.update(app.config)
    mail.init_app(app)

    # error handlers
    initialize_error_handlers(app)

    # jwt
    JWTManager(app)

    # bind app to db
    db.init_app(app)

    import api.models
    import api.views

    # celery tasks
    import celery_conf.tasks  # noqa: F401

    # initialize migration scripts
    migrate = Migrate(compare_type=True)
    migrate.init_app(app, db)

    return app


@api.errorhandler(ValidationError)
@middleware_blueprint.app_errorhandler(ValidationError)
def handle_exception(error):
    """Error handler called when a ValidationError Exception is raised"""

    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
