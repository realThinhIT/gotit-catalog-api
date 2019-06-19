class _Config(object):
    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False          # Disable tracking of objects and improve performance
    SQLALCHEMY_ECHO = False                         # To log SQL statements for debugging

    # Flask
    SECRET_KEY = 'THINHND123456@FLASK'              # To provide authentication abilities
    DEBUG = False                                   # For Flask to give useful error pages

    # Flask-Bcrypt
    BCRYPT_LOG_ROUNDS = 10                          # Hashing rounds for passwords

