from flask import jsonify
from main import app
from main.models import UserModel
from main.errors import DuplicatedResourceError
from main.libs.resource_parsing.common import parse_with_schema
from main.schemas.user import UserSchema
from main.libs.encryption.password import update_password_hash_in_dict


@app.route('/users', methods=['POST'])
@parse_with_schema(UserSchema())
def register_user(data):
    """
    Register a new user into the database

    :return: new User instance except for password
    """

    # Check if user did exist
    duplicated_user = UserModel.find_user_by_username_or_email(
        data.get('username'),
        data.get('email')
    )

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

    # Tell user which field is duplicated
    if duplicated_user:
        errors = {}

        if duplicated_user.email == data.get('email'):
            errors.update(email_error)

        if duplicated_user.username == data.get('username'):
            errors.update(username_error)

        raise DuplicatedResourceError(errors)

    # Proceed to create new user
    data = update_password_hash_in_dict(data)

    new_user = UserModel(**data)
    new_user.save()

    return jsonify(
        UserSchema().dump(new_user)
    )
