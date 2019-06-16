import datetime
import jwt
import functools
from flask import request
from flask_bcrypt import Bcrypt
from main import app
from main.config import config
from main.models.user import UserModel
from main.errors import UnauthorizedError


# Define bcrypt encryption
bcrypt = Bcrypt(app)


def generate_token(subject):
    """
    Generate JWT Token for authentication.

    :param subject: User instance
    :return: JWT Token string
    """

    iat = datetime.datetime.utcnow()

    return jwt.encode({
        'sub': subject.id,                          # Subject of this token
        'iat': iat,                                 # Issued at
        'exp': iat + datetime.timedelta(days=30)    # Expires at
    }, config.SECRET_KEY)


def decode_token(access_token):
    """
    Decode & verify token received during authorization.

    :param access_token: Access token of the user
    :return: token payload if it's available, None if it's not valid
    """

    try:
        token = jwt.decode(
            access_token,
            config.SECRET_KEY,
            leeway=10,                              # To keep token available after expiration a short amount of time
            verify=True
        )
    except jwt.InvalidTokenError:
        return None

    return token


def verify_user_by_username_and_password(username, password):
    """
    Find user by username and verify its password.

    :param username: Username of the user
    :param password: Password of the user in plaintext
    :return: User instance corresponds to the user, or None
    """

    user = UserModel.query.filter_by(username=username).first()

    if user and user.password_hash and bcrypt.check_password_hash(user.password_hash, password):
        return user
    else:
        return None


def get_subject_user():
    """
    Identity handler for JWT.
    To help JWT to retrieve user's information based on the subject from the payload.

    :return: User instance if that user is available
    """

    # Extract Authorization header from headers
    authorization = None

    if 'Authorization' in request.headers:
        authorization = request.headers['Authorization']

    # If Authorization is not used or not provided, return None
    if not authorization:
        return None

    # If Authorization type is not Bearer, return None
    if not authorization.startswith('Bearer '):
        return None

    # Extract access_token from the header
    access_token = decode_token(authorization[len('Bearer '):])

    # If token is invalid, expired or cannot be decoded
    if not access_token:
        return None

    # Retrieve user's information from the payload['subject'] and then return an User instance
    user_id = access_token['sub']

    return UserModel.find_by_id(user_id)


def requires_authentication(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        # Retrieve responding user
        user = get_subject_user()

        # In case token is valid and user is available,
        # pass an user argument to the function
        if user:
            kwargs['user'] = user
            return func(*args, **kwargs)

        # If user is unavailable
        else:
            raise UnauthorizedError()
    return decorator


def optional_authentication(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        # Retrieve responding user
        user = get_subject_user()

        # Pass user to the argument
        kwargs['user'] = user
        return func(*args, **kwargs)
    return decorator

