from flask import jsonify

from main import app, bcrypt
from main.models import UserModel
from main.errors import DuplicatedResourceError
from main.schemas.user import UserSchema
from main.libs.resource_parsing.common import parse_with_schema


@app.route('/users', methods=['POST'])
@parse_with_schema(UserSchema())
def register_user(data):
    """Register a new user into the database

    :return: new User instance except for password
    """

    # Check if user did exist
    duplicated_user = UserModel.find_user_by_username_or_email(
        data.get('username'),
        data.get('email')
    )

    # Tell user which field is duplicated
    if duplicated_user:
        errors = {}

        # Define errors
        email_error = {
            'email': [
                'Email is registered.'
            ]
        }

        username_error = {
            'username': [
                'Username is registered.'
            ]
        }

        # Update errors
        if duplicated_user.email == data.get('email'):
            errors.update(email_error)

        if duplicated_user.username == data.get('username'):
            errors.update(username_error)

        raise DuplicatedResourceError(errors)

    # Proceed to create new user
    data.update({
        'encrypted_password': bcrypt.generate_password_hash(data.get('password'))
    })
    data.pop('password')

    # Create a new user
    new_user = UserModel(**data)
    new_user.save()

    return jsonify(
        UserSchema().dump(new_user)
    )
