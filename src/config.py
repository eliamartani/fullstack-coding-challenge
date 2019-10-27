import os
import sys

if os.path.exists('.env'):
    print('Importing environment from .env file')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1].replace("\"", "")

class Config:
    # APP
    APP_NAME = os.environ.get('APP_NAME', '')

    # API Key
    API_USERNAME = os.environ.get('API_USERNAME', '')
    API_KEY = os.environ.get('API_KEY', '')

    # Database
    DB_HOST = os.environ.get('DB_HOST', '')
    DB_DATABASE = os.environ.get('DB_DATABASE', '')
    DB_USERNAME = os.environ.get('DB_USERNAME', '')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True

    @classmethod
    def init_app(cls, app):
        print('DEVELOP MODE.')


class TestingConfig(Config):
    TESTING = True

    @classmethod
    def init_app(cls, app):
        print('TESTING MODE.')


class ProductionConfig(Config):
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
