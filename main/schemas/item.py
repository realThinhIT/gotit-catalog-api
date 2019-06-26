from marshmallow import fields, validate

from main.schemas.base import BaseSchema


class ItemSchema(BaseSchema):
    """Schema for Item objects"""

    name = fields.String(
        required=True,
        validate=[
            validate.Length(1, 64, 'Name is required and must be between 1 - 64 characters.')
        ],
        error_messages={
            'required': 'Item name is required.'
        }
    )
    description = fields.String()

    is_owner = fields.Boolean(
        dump_only=True
    )
