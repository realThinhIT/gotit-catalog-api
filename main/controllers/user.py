from main import app
from main.request import validate_with_schema
from main.response import json_response
from main.schemas.user import UserSchema
from main.models import UserModel
from main.errors import DuplicatedResourceError, InternalServerError


@app.route('/users', methods=['POST'])
@validate_with_schema(UserSchema())
@json_response
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

    if duplicated_user:
        raise DuplicatedResourceError()

    # Proceed to create new user
    try:
        new_user = UserModel(**data)
        new_user.save()
    except Exception:
        raise InternalServerError()

    return UserSchema().dump(new_user)
