from flask import jsonify
from main import app
from main.errors import InvalidCredentialsError
from main.schemas.authentication import RequestUserAuthenticationSchema, ResponseAuthenticationSchema
from main.request import validate_with_schema
from main.security import verify_user_by_username_and_password, generate_token


@app.route('/authentication', methods=['POST'])
@validate_with_schema(RequestUserAuthenticationSchema())
def authenticate(data):
    """
    Authenticate user and generate a token for authenticating following requests.

    :param data: Valid user schema
    :return: A JWT access token
    """

    user = verify_user_by_username_and_password(
        username=data.get('username'),
        password=data.get('password')
    )

    if user:
        return jsonify(
            ResponseAuthenticationSchema().load({
                'access_token': generate_token(user)
            })
        ), 200
    else:
        raise InvalidCredentialsError()
