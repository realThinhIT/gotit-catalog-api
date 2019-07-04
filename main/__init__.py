from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt

import main.models
from main.config import config
from main.database import db
from main.errors import NotFoundError, InternalServerError, MethodNotAllowed
from main.controllers import init_routes

# Create app instance associated with the module that runs it
app = Flask(__name__)

# Load configurations corresponding to environment
app.config.from_object(config)

# Define bcrypt encryption
bcrypt = Bcrypt(app)

# Init DB
db.init_app(app)

# Initialize database using Flask-SQLAlchemy
db.create_all(app=app)

# Init routes
init_routes()


# Errors handlers
def _response_error(exception=None):
    """To manipulate structure of response payload.

    :param exception: Exception instance for errors
    :return: flask.Response instance
    """

    prepared_data = {
        'error_code': exception.error_code,
        'message': exception.message
    }

    if exception.errors != {}:
        prepared_data['errors'] = exception.errors

    return jsonify(prepared_data), exception.status_code


@app.errorhandler(errors.Error)
def handle_error(exception):
    return _response_error(exception=exception)


@app.errorhandler(404)
def page_not_found(*_):
    return _response_error(exception=NotFoundError())


@app.errorhandler(405)
def method_not_allowed(*_):
    return _response_error(exception=MethodNotAllowed())


@app.errorhandler(500)
def internal_server_error(*_):
    return _response_error(exception=InternalServerError())


# Allow CORS for API requests
@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Methods'] = '*'
    header['Access-Control-Allow-Headers'] = '*'

    if request.method == 'OPTIONS':
        response.status_code = 200

    return response
