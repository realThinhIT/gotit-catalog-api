import functools
from flask import request
from main.errors import UnauthorizedError
from main.models.user import UserModel
from main.libs.encryption.jwttoken import decode_token


def _get_user_from_token():
    """Identity handler for JWT.
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


def require_authentication(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        # Retrieve responding user
        user = _get_user_from_token()

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
        user = _get_user_from_token()

        # Pass user to the argument
        kwargs['user'] = user
        return func(*args, **kwargs)
    return decorator
