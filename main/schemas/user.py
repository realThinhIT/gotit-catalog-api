import re
from marshmallow import fields, validate, ValidationError
from .base import BaseSchema


def _validate_username(string):
    regex = re.compile('^[A-Za-z0-9]+$')
    if not regex.match(string):
        raise ValidationError('Username must contain only lowercase letters and numbers.')


class UserSchema(BaseSchema):
    """
    Schema for User objects
    """

    id = fields.Integer()
    username = fields.String(
        required=True,
        validate=[
            _validate_username,
            validate.Length(5, 30, 'Username must be between 5 - 30 characters.')
        ],
        error_messages={
            'required': 'Username is required.'
        }
    )
    email = fields.Email(
        required=True,
        error_messages={
            'required': 'Email is required.'
        }
    )
    name = fields.String(
        required=True,
        validate=[
            validate.Length(1, 64, 'Name is required.')
        ],
        error_messages={
            'required': 'Name is required.'
        }
    )
    password = fields.String(
        required=True,
        validate=[
            validate.Length(6, 64, 'Password must be at least 6 characters.')
        ],
        error_messages={
            'required': 'Password is required.'
        },
        load_only=True
    )
    password_hash = fields.String(
        load_only=True
    )


