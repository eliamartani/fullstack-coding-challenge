import os

from flask import Flask
from flask_assets import Environment
from flask_compress import Compress
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from app.assets import app_css, app_js
from config import config as Config

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
compress = Compress()
csrf = CSRFProtect()

def create_app(env_name):
    app = Flask(__name__)
    app_env = env_name

    # Load config
    app.config.from_object(Config[app_env])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # Initialize config
    Config[app_env].init_app(app)

    # Initialize extensions
    db.init_app(app)
    compress.init_app(app)
    csrf.init_app(app)

    # Initialize asset pipeline
    assets_env = Environment(app)
    dirs = ['assets/scss', 'assets/js']

    # Append frontend files
    for path in dirs:
        assets_env.append_path(os.path.join(basedir, path))

    assets_env.register('app_css', app_css)
    assets_env.register('app_js', app_js)

    # Create app blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
