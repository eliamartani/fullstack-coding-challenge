import os

from flask import Flask
from flask_assets import Environment
from app.assets import app_css, app_js
from config import config as Config

basedir = os.path.abspath(os.path.dirname(__file__))

def create_app(config):
    app = Flask(__name__)
    config_name = config

    if not isinstance(config, str):
        config_name = os.getenv('FLASK_CONFIG', 'default')

    app.config.from_object(Config[config_name])

    Config[config_name].init_app(app)

    # Set up asset pipeline
    assets_env = Environment(app)
    dirs = ['assets/scss', 'assets/js']

    for path in dirs:
        assets_env.append_path(os.path.join(basedir, path))

    assets_env.register('app_css', app_css)
    assets_env.register('app_js', app_js)

    # Create app blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
