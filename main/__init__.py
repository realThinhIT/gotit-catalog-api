from flask import Flask
from flask_bcrypt import Bcrypt
from marshmallow import ValidationError
from main.config import config
from main.security import init_jwt
from main.response import Response
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

# To initialize database using Flask-SQLAlchemy
@app.before_first_request
def init_db():
    import main.models
    db.create_all()


# Errors handlers
@app.errorhandler(errors.Error)
def handle_error(exception):
    return Response.output_exception_json(exception=exception)


@app.errorhandler(404)
def page_not_found(error):
    return Response.output_exception_json(exception=errors.InvalidResourceError(error.message))


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
