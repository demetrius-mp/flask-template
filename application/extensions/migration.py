from flask import Flask
from flask_migrate import Migrate

from application.extensions.database import db

migrate = Migrate()


def init_app(app: Flask):
    migrate.init_app(app, db)
