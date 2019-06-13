from flask import Flask, request
from flask_restful import Api
from flask_bcrypt import Bcrypt
from marshmallow import ValidationError
from main.config import config
from main.resources import add_resources
from main.security import init_jwt
from main.response import ExceptionResponse
from main.database import db
from main.schemas.user import UserAuthenticationSchema
import main.errors

# Create app instance associated with the module that runs it
app = Flask(__name__)

# Load configurations corresponding to environment
app.config.from_object(config)

# Setup JWT authentication & Bcrypt encryption
init_jwt(app)
bcrypt = Bcrypt(app)

# Create routes
api = Api(app)
add_resources(api)

# # Manipulate response payloads
# @api.representation('application/json')
# def make_response(*args, **kwargs):
#     return Response.output_json(*args, **kwargs)


# To initialize database using Flask-SQLAlchemy
@app.before_first_request
def init_db():
    from main.models import *
    db.create_all()


# Errors handlers
@app.errorhandler(errors.Error)
def handle_error(exception):
    return ExceptionResponse.output_json(exception=exception)


@app.errorhandler(404)
def page_not_found():
    raise errors.NotFoundError()


@app.errorhandler(400)
def bad_request():
    raise errors.BadRequestError()


@app.errorhandler(500)
def internal_server_error():
    raise errors.InternalServerError()

# Handle custom routes
@app.before_request
def require_authorization():
    from flask import request

    # Process request payload for authentication
    if request.endpoint == '_default_auth_request_handler':
        try:
            UserAuthenticationSchema().load(request.get_json() or {})
        except ValidationError, err:
            raise errors.InputValidationError(err.messages)
