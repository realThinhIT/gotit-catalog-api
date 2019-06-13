from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from main.config import config
from main.resources import add_resources
from main.security import init_jwt
from main.response import SuccessResponse

# Create app instance associated with the module that runs it
app = Flask(__name__)

# Load configurations corresponding to environment
app.config.from_object(config)

# Init database
db = SQLAlchemy(
    app=app
)

# Setup JWT authentication & Bcrypt encryption
init_jwt(app)
bcrypt = Bcrypt(app)

# Create routes
api = Api(app)
add_resources(api)

# Manipulate response payloads
@api.representation('application/json')
def make_response(*args, **kwargs):
    return SuccessResponse.output_json(*args, **kwargs)
