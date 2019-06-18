from main.config.base import _Config


class _DevelopmentConfig(_Config):
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:thinhnd@127.0.0.1:3306/catalog_dev'
    SQLALCHEMY_ECHO = True

    # Flask
    DEBUG = True


config = _DevelopmentConfig
