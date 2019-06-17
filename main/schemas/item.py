from marshmallow import Schema, fields, validate
from .base import BaseSchema


class ItemSchema(BaseSchema):
    id = fields.Integer()
    name = fields.String(
        required=True,
        validate=[
            validate.Length(1, 64, 'Name is required and must be between 1 - 64 characters.')
        ]
    )
    description = fields.String()

    is_owner = fields.Boolean(
        dump_only=True
    )


class ItemSchemaRequest(Schema):
    name = fields.String(
        required=True,
        validate=[
            validate.Length(1, 64, 'Name is required and must be between 1 - 64 characters.')
        ]
    )
    description = fields.String()
