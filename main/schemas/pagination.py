from marshmallow import Schema, fields


class RequestPaginationSchema(Schema):
    page = fields.Integer(default=1, missing=1)
    per_page = fields.Integer(default=50, missing=50)


class ResponsePaginationSchema(Schema):
    items = fields.Raw()

    page = fields.Integer()
    per_page = fields.Integer()
    total_pages = fields.Integer()
    total = fields.Integer()
    has_next = fields.Boolean()
