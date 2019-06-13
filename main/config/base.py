import datetime


class _Config(object):
    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = True           # Disable tracking of objects and improve performance
    SQLALCHEMY_ECHO = False                         # To log SQL statements for debugging

    # Flask
    SECRET_KEY = 'THINHND123456@'                   # To provide authentication abilities
    DEBUG = False                                   # For Flask to give useful error pages

    # Flask-Bcrypt
    BCRYPT_LOG_ROUNDS = 10                          # Hashing rounds for passwords

    # Flask-JWT
    JWT_AUTH_URL_RULE = '/authentication'            # Set authentication endpoint
    JWT_EXPIRATION_DELTA = datetime.timedelta(       # Set expire after 30 days
        days=30
    )
