from flask import Flask
import logging
from main.config import config
from main.response import Response
from main.database import db
from main.models import *
from main.errors import NotFoundError, InternalServerError, MethodNotAllowed

# Create app instance associated with the module that runs it
app = Flask(__name__)

# Load configurations corresponding to environment
app.config.from_object(config)

# Init DB
db.init_app(app)

# To initialize database using Flask-SQLAlchemy
@app.before_first_request
def init_db():
    import main.models
    db.create_all()

# Errors handlers
# TODO: Add more handlers
@app.errorhandler(errors.Error)
def handle_error(exception):
    return Response.output_exception_json(exception=exception)


@app.errorhandler(404)
def page_not_found(error):
    return Response.output_exception_json(exception=NotFoundError())


@app.errorhandler(405)
def method_not_allowed(error):
    return Response.output_exception_json(exception=MethodNotAllowed())


@app.errorhandler(500)
def internal_server_error(error):
    return Response.output_exception_json(exception=InternalServerError())
