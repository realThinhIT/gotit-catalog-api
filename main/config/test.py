from .base import _Config


class _TestConfig(_Config):
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:thinhnd@127.0.0.1:3306/catalog_test'

    # Flask
    DEBUG = False

    # PyTest
    TESTING = True


config = _TestConfig
