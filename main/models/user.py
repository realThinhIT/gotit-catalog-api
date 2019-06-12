from main.models.base import BaseModel
from sqlalchemy import Column, String
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
    def verify_user_by_username_and_password(cls, username, password):
        user = cls.query.filter_by(username=username).first()

        if user and user.password and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return None
