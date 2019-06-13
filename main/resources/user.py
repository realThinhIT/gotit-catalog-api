from flask_restful import Resource, request
from ..models.user import UserModel
from ..schemas.user import UserSchema
from marshmallow import ValidationError
from main.errors import InputValidationError, DuplicatedResourceError, InternalServerError


class UserResource(Resource):
    """
    User Resource
    """
    schema = UserSchema()

    def post(self):
        """
        To register a new user into the database

        :return: new User instance except for password
        """

        data = request.get_json() or {}

        # Try to validate the payload
        try:
            self.schema.load(data)
        except Exception, err:
            raise InputValidationError(err.messages)

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

        return self.schema.dump(new_user), 200

