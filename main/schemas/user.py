from marshmallow import Schema, fields, validate
from .base import BaseSchema


class UserSchema(BaseSchema):
    """
    Schema for User objects
    """

    id = fields.Integer()
    username = fields.String(
        required=True,
        validate=[
            validate.Length(5, 30, 'Username must be between 5 - 30 characters.')
        ]
    )
    email = fields.Email(
        required=True
    )
    name = fields.String(
        required=True,
        validate=[
            validate.Length(1, 64, 'Name is required.')
        ]
    )
    password = fields.String(
        required=True,
        validate=[
            validate.Length(6, 64, 'Password must be at least 6 characters.')
        ],
        load_only=True
    )


class UserAuthenticationSchema(Schema):
    """
    Schema for User while performing authentication
    """

    username = fields.String(
        required=True
    )
    password = fields.String(
        required=True
    )
