import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event

db = SQLAlchemy()


def init_app(app: Flask):
    if 'SQLALCHEMY_DATABASE_URI' not in app.config:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
                                                os.environ.get('DATABASE_URL') or \
                                                'sqlite:///storage.db'

    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    if db_uri.startswith('postgres'):
        conn_str = db_uri.split('://')[1]
        database_url = f'postgresql+psycopg2://{conn_str}'
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url

    db.init_app(app)

    with app.app_context():
        if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
            event.listen(db.engine, 'connect', lambda con, rec: con.execute('pragma foreign_keys=ON'))
