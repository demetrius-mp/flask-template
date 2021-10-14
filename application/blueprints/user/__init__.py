from flask import Flask

from application.blueprints.user.routes import users


def init_app(app: Flask):
    app.register_blueprint(users)
