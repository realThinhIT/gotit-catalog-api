from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import main.models
from main.config import config
from main.database import db
from main.errors import NotFoundError, InternalServerError, MethodNotAllowed
from main.controllers import init_routes
from main.libs.response import output_exception_json

# Create app instance associated with the module that runs it
app = Flask(__name__)

# Load configurations corresponding to environment
app.config.from_object(config)

# Allow CORS for API requests
CORS(app)

# Define bcrypt encryption
bcrypt = Bcrypt(app)

# Init DB
db.init_app(app)

# Initialize database using Flask-SQLAlchemy
db.create_all(app=app)

# Init routes
init_routes()


# Errors handlers
@app.errorhandler(errors.Error)
def handle_error(exception):
    return output_exception_json(exception=exception)


@app.errorhandler(404)
def page_not_found(*_):
    return output_exception_json(exception=NotFoundError())


@app.errorhandler(405)
def method_not_allowed(*_):
    return output_exception_json(exception=MethodNotAllowed())


@app.errorhandler(500)
def internal_server_error(*_):
    return output_exception_json(exception=InternalServerError())
