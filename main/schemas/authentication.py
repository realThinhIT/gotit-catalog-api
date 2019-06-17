from marshmallow import Schema, fields


class RequestUserAuthenticationSchema(Schema):
    """
    Schema for User while performing authentication
    """

    username = fields.String(
        required=True,
        error_messages={
            'required': 'Username is required.'
        }
    )
    password = fields.String(
        required=True,
        error_messages={
            'required': 'Password is required.'
        }
    )


class ResponseAuthenticationSchema(Schema):
    """
    Schema for Access Token response while performing authentication
    """

    access_token = fields.String()
