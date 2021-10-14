import os

from flask import Flask

from application.extensions import configuration


def create_app():
    app = Flask(__name__)
    configuration.init_app(app)
    if not app.secret_key:
        app.secret_key = os.environ.get('SECRET_KEY', 'unsafe-secret-key')

    return app
