from flask import jsonify
from main import app
from main.request import validate_with_schema
from main.schemas.user import UserSchema
from main.models import UserModel
from main.errors import DuplicatedResourceError, InternalServerError
from main.utils.password import update_password_hash_in_dict


@app.route('/users', methods=['POST'])
@validate_with_schema(UserSchema())
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

    # Tell user which field is duplicated
    if duplicated_user:
        if duplicated_user.email == data.get('email'):
            raise DuplicatedResourceError({
                'email': [
                    'Email is registered.'
                ]
            })
        else:
            raise DuplicatedResourceError({
                'username': [
                    'Username is registered.'
                ],
            })

    # Proceed to create new user
    try:
        data = update_password_hash_in_dict(data)

        new_user = UserModel(**data)
        new_user.save()
    except Exception:
        raise InternalServerError()

    return jsonify(
        UserSchema().dump(new_user)
    ), 200
