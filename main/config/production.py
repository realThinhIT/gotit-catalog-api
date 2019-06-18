from main.config.base import _Config


class _ProductionConfig(_Config):
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:thinhnd@127.0.0.1:3306/catalog_prod'

    # Flask
    DEBUG = False

    # PyTest
    TESTING = False


config = _ProductionConfig
