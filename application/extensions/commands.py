from flask import Flask

from application.extensions.auth import generate_password_hash
from application.extensions.database import db
from application.models import User, Role


def drop_db_():
    db.drop_all()


def populate_db_():
    role = Role(name='Administrador', description='Descrição do papel aqui.')
    db.session.add(role)

    pw_hash = generate_password_hash('admin')
    # noinspection PyArgumentList
    admin = User(email='admin@admin.com', name='Admin Admin', password=pw_hash, is_active=True, role_id=1)
    db.session.add(admin)

    db.session.commit()


def init_app(app: Flask):
    @app.cli.command()
    def drop_db():
        """Drops all the tables in the database"""
        drop_db_()

    @app.cli.command()
    def populate_db():
        """Populates the database with the needed rows"""
        populate_db_()
