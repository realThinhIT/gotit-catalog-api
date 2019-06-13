from main.models.base import BaseModel
from sqlalchemy import Column, String, or_
from main import bcrypt


class UserModel(BaseModel):
    __tablename__ = 'users'

    username = Column(String(30), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)

    def __init__(self, username, email, name, password):
        self.username = username
        self.email = email
        self.name = name
        self.password = bcrypt.generate_password_hash(password)

    @classmethod
    def find_user_by_username_or_email(cls, username='', email=''):
        """
        To find user by username and verify its password.

        :param username: Username of the user
        :param email: Email of the user
        :return: User instance corresponds to the user, or None
        """

        user = cls.query.filter(or_(
            cls.username == username,
            cls.email == email
        )).first()

        if user:
            return user
        else:
            return None

    @classmethod
    def verify_user_by_username_and_password(cls, username, password):
        """
        To find user by username and verify its password.

        :param username: Username of the user
        :param password: Password of the user in plaintext
        :return: User instance corresponds to the user, or None
        """

        user = cls.query.filter_by(username=username).first()

        if user and user.password and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return None
