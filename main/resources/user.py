from marshmallow import Schema, fields


class UserSchema(Schema):
    """
    Schema for User objects
    """

    id = fields.Integer()
    username = fields.String(
        required=True,
        error_messages={
            'required': 'Username is required.'
        },
        validate=UserError.validate_username)
    email = fields.Email(
        required=True,
        error_messages={'required': 'Email is required.'},
        validate=UserError.validate_email)
    name = fields.String(
        required=True,
        error_messages={'required': 'Name is required.'},
        validate=UserError.validate_name)
    password = fields.String(
        required=True,
        error_messages={'required': 'Password is required.'},
        validate=UserError.validate_password,
        load_only=True)