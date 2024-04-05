import os

class Config:
    DIR = os.path.dirname(os.path.abspath(__file__))
    TESTING = False
    DEBUG = True
    DATABASE_NAME = 'bud_buddies'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'
    ENVIRONMENT = 'production'
    DEBUG = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(os.path.join(Config.DIR, "tmp", f'{Config.DATABASE_NAME}.db'))
    ENVIRONMENT = 'development'

    # Create Development Database if it doesn't exist
    if not os.path.exists(os.path.join(Config.DIR, "tmp")):
        os.makedirs(os.path.join(Config.DIR, "tmp"))
    if not os.path.exists(os.path.join(Config.DIR, "tmp", f'{Config.DATABASE_NAME}.db')):
        with open(os.path.join(Config.DIR, "tmp", f'{Config.DATABASE_NAME}.db'), 'w') as f:
            f.write("")

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    ENVIRONMENT = 'test'
    TESTING = True