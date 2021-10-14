from flask import Flask
from flask_admin import Admin
from flask_admin.menu import MenuLink

from application import models
from application.extensions.admin import views
from application.extensions.auth import current_user
from application.extensions.database import db

admin = Admin()


class LogoutMenuLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated


admin.add_link(LogoutMenuLink(name='Sair', category='', url='/logout'))


def init_app(app: Flask):
    admin.name = app.config.TITLE
    admin.template_mode = "bootstrap3"
    admin.init_app(app)
    admin.add_view(views.UserView(models.User, db.session, name='Usuários'))
