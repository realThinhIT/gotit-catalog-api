import datetime
import jwt
from main.config import config


def generate_token(user):
    """
    Generate JWT Token for authentication.

    :param user: User instance
    :return: JWT Token string
    """

    iat = datetime.datetime.utcnow()

    return jwt.encode({
        'sub': user.id,                             # Subject of this token
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
        payload = jwt.decode(
            access_token,
            config.SECRET_KEY,
            leeway=10,                              # To keep token available after expiration a short amount of time
            verify=True
        )
    except jwt.InvalidTokenError:
        return None

    return payload
