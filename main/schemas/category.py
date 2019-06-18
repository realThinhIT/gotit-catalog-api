from marshmallow import fields, validate
from main.schemas.base import BaseSchema


class CategorySchema(BaseSchema):
    """Schema for Category objects"""

    name = fields.String(
        required=True,
        nullable=False,
        validate=[
            validate.Length(1, 64, 'Category name must be between 1 - 64 characters')
        ],
        error_messages={
            'required': 'Category name is required.'
        }
    )
    description = fields.String()
