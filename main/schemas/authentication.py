from marshmallow import Schema, fields


class RequestUserAuthenticationSchema(Schema):
    """
    Schema for User while performing authentication
    """

    username = fields.String(
        required=True
    )
    password = fields.String(
        required=True
    )


class ResponseAuthenticationSchema(Schema):
    """
    Schema for Access Token response while performing authentication
    """

    access_token = fields.String()
