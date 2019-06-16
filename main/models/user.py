from sqlalchemy import Column, String, or_
from main.models.base import BaseModel
from main.database import db


class UserModel(BaseModel):
    __tablename__ = 'user'

    username = Column(String(30), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(64), nullable=False)
    password_hash = Column(String(64), nullable=False)

    # Define relationships
    items = db.relationship('ItemModel', back_populates='user', lazy='dynamic')

    # None-sql fields
    password = None

    def __init__(self, username, email, name, password_hash):
        self.username = username
        self.email = email
        self.name = name
        self.password_hash = password_hash

    @classmethod
    def find_user_by_username_or_email(cls, username='', email=''):
        """
        Find user by username and verify its password.

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
