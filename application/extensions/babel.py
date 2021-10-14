from flask import Flask
from flask_babelex import Babel

babel = Babel()


def init_app(app: Flask):
    babel.init_app(app)
