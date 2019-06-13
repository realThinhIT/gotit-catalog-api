from flask_jwt import JWT


def authenticate_handler(username, password):
    """
    Authentication handler for JWT
    To help JWT to authenticate users using their username and password

    :param username: username of the user
    :param password: password of the user
    :return: User instance if that user is available
    """

    from main.models.user import UserModel

    return UserModel.verify_user_by_username_and_password(username, password)


def identity_handler(payload):
    """
    Identity handler for JWT
    To help JWT to retrieve user's information based on identity from the payload

    :param payload: payload of the identity
    :return: User instance if that user is available
    """

    from main.models.user import UserModel

    # Retrieve user's identity from the payload and then return a
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)


def init_jwt(app):
    return JWT(app=app,
               authentication_handler=authenticate_handler,
               identity_handler=identity_handler)
