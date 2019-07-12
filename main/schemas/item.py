import re

from marshmallow import fields, validate, ValidationError

from main.schemas.base import BaseSchema


# def _validate_name(string):
#     regex = re.compile("^[A-Za-z0-9.,'\"?!/]+(?: +[A-Za-z0-9.,\"'?!/)()]+)*$")
#     if not regex.match(string):
#         raise ValidationError('Item name must not contain trailing whitespaces and some special characters.')


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