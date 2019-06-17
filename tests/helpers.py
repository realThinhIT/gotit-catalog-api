import json
import datetime
import jwt
import string
import random
from main.config import config
from main.utils.database import execute_sql_from_file


def create_mock_data():
    execute_sql_from_file('./sql/test.sql')


def drop_tables():
    execute_sql_from_file('./sql/drop_tables.sql')


def create_headers(access_token=None):
    headers = {
        'Content-Type': 'application/json'
    }

    if access_token:
        headers.update({
            'Authorization': 'Bearer {}'.format(access_token)
        })

    return headers


def json_response(response):
    return json.loads(response.data.decode('utf-8'))


def generate_access_token(user_id, is_expired=False):
    """
    Generate JWT Token for test authentication.

    :param user_id: User ID
    :param is_expired: To generate expired tokens
    :return: JWT Token string
    """

    iat = datetime.datetime.utcnow()

    return jwt.encode({
        'sub': user_id,                             # Subject of this token
        'iat': iat,                                 # Issued at
        'exp': iat + datetime.timedelta(hours=1) if not is_expired else iat-11     # Expired at
    }, config.SECRET_KEY)


def random_string(string_length=10):
    """Generate a random string of fixed length"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))