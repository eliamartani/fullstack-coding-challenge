import os
import sys

if os.path.exists('.env'):
    print('[config] Importing environment from .env file')

    for line in open('.env'):
        var = line.strip().split('=')

        if len(var) == 2:
            os.environ[var[0]] = var[1].replace("\"", "")

class Config:
    # APP
    APP_NAME = os.getenv('APP_NAME', '')

    # Unbabel API
    UNBABEL_USERNAME = os.getenv('UNBABEL_USERNAME', '')
    UNBABEL_KEY = os.getenv('UNBABEL_KEY', '')
    UNBABEL_SANDBOX = os.getenv('UNBABEL_SANDBOX', False)
    UNBABEL_SOURCE = os.getenv('UNBABEL_SOURCE', '')
    UNBABEL_TARGET = os.getenv('UNBABEL_TARGET', '')

    # Database
    DATABASE_URI = os.getenv('DATABASE_URI', '')

    # SQL Alchemy
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', '')

    # CSRF
    SECRET_KEY = os.getenv('SECRET_KEY', '')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    ASSETS_DEBUG = True
    DEBUG = True
    DEVELOPMENT = True

    @classmethod
    def init_app(cls, app):
        print('[config] DEVELOP MODE')


class TestingConfig(Config):
    TESTING = True

    @classmethod
    def init_app(cls, app):
        print('[config] TESTING MODE')


class ProductionConfig(Config):
    DEBUG = False

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
