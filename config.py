import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KET = 'seekrat -- keaze'
    SQLACHEMY_DATABASE_URL = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    pass


class StagingConfig(Config):
    DEBUG = True
    DEVELOPMENT = True


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True


class TestingConfig(Config):
    TESTING = True
