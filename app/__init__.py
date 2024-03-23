from flask import Flask
from config import Config
from .cyanite import cyanite as cyanite_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(cyanite_blueprint, url_prefix='/cyanite')
    return app
