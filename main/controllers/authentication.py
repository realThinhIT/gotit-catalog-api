from flask import jsonify

from main import app, bcrypt
from main.errors import InvalidCredentialsError
from main.models.user import UserModel
from main.schemas.authentication import RequestUserAuthenticationSchema, ResponseUserAuthenticationSchema
from main.libs.resource_parsing.common import parse_with_schema
from main.libs.jwttoken import generate_token


@app.route('/authentication', methods=['POST'])
@parse_with_schema(RequestUserAuthenticationSchema())
def authenticate(data):
    """Authenticate user and generate a token for authenticating following requests.

    :param data: Valid user schema
    :return: A JWT access token
    """

    user = UserModel.query.filter_by(username=data.get('username')).first()

    if user and user.encrypted_password and bcrypt.check_password_hash(user.encrypted_password, data.get('password')):
        return jsonify(
            ResponseUserAuthenticationSchema().load({
                'access_token': generate_token(user)
            })
        )
    else:
        raise InvalidCredentialsError()
