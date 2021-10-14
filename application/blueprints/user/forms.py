from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    """Form to login a user."""
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember = BooleanField('Lembre-se de mim.')
    submit = SubmitField('Login')


class ResetPasswordForm(FlaskForm):
    """Form to reset a user's password."""
    password = PasswordField('Nova senha', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirmar nova senha',
        validators=[
            DataRequired(), EqualTo('password', message='Este campo deve ser igual a senha')
        ]
    )
    submit = SubmitField('Redefinir senha')
