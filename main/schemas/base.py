from marshmallow import Schema, fields


class BaseSchema(Schema):
    """
    Base Schema for others
    """

    id = fields.Integer()
    updated = fields.DateTime()
    created = fields.DateTime()
