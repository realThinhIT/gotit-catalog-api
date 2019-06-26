from marshmallow import Schema, fields, validate


class RequestPaginationSchema(Schema):
    """Schema for validating pagination query strings"""

    page = fields.Integer(
        default=1,
        missing=1,
        validate=validate.Range(min=1)
    )
    per_page = fields.Integer(
        default=50,
        missing=50,
        validate=validate.Range(min=1, max=200)
    )


class ResponsePaginationSchema(Schema):
    """Schema for serving items with pagination"""

    items = fields.Raw()

    page = fields.Integer()
    per_page = fields.Integer()
    total_pages = fields.Integer()
    total = fields.Integer()
