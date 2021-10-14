from flask import flash, Markup, url_for
from flask_admin.actions import action
from flask_admin.form import rules
from wtforms import PasswordField
from wtforms.validators import DataRequired, EqualTo

from application import models
from application.extensions.admin.views.base import BaseView
from application.extensions.auth import generate_password_hash, current_user


class UserView(BaseView):
    column_list = ('email', 'name', 'role', 'is_active')
    form_extra_fields = {
        'confirm_password': PasswordField(
            'Confirmar senha', validators=[
                DataRequired(), EqualTo('password', message='Este campo deve ser igual a senha')
            ]
        ),
        'password': PasswordField(
            'Senha', validators=[
                DataRequired()
            ]
        )
    }

    column_labels = {
        'email': 'Email',
        'name': 'Nome completo',
        'role': 'Papel',
        'is_active': 'Ativado',
    }

    form_edit_rules = [
        rules.Field('role'),
        rules.Field('name'),
        rules.Field('email'),
        rules.Field('is_active'),
    ]

    form_create_rules = [
        rules.Field('role'),
        rules.Field('name'),
        rules.Field('email'),
        rules.Field('password'),
        rules.Field('confirm_password'),
        rules.Field('is_active'),
    ]

    def on_model_change(self, form, model: models.User, is_created):
        if is_created:
            model.password = generate_password_hash(model.password)

    def is_accessible(self):
        accessible_by_roles = (1,)
        return current_user.role_id in accessible_by_roles

    @action(
        name='reset_password_link',
        text='Gerar link para redefinir senha',
        confirmation='Tem certeza?'
    )
    def generate_reset_password_link(self, ids: list[int]):
        # noinspection PyUnresolvedReferences
        for user in models.User.query.filter(models.User.id.in_(ids)):
            reset_password_token = user.get_reset_password_token()
            reset_password_link = url_for('users.reset_password', token=reset_password_token)
            flash_message = Markup(
                f'<a href="{reset_password_link}">Clique neste link</a> para redefinir a senha do usuário {user.email}.'
            )
            flash(flash_message, 'success')
