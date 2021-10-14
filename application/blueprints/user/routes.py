from flask import Blueprint, flash, redirect, url_for, request, render_template
from sqlalchemy.orm import Session

from application.blueprints.user.forms import LoginForm, ResetPasswordForm
from application.extensions import auth
from application.extensions.database import db
from application.models import User

users = Blueprint('users', __name__, template_folder='templates')


@users.route("/login", methods=['GET', 'POST'])
def login():
    """Route to login a user."""
    if auth.current_user.is_authenticated:
        return redirect(url_for('admin.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and not user.is_active:
            flash('Sua conta está desativada.', 'warning')
            return redirect(url_for('users.login'))

        if user and auth.check_password_hash(user.password, form.password.data):
            auth.login_user(user, remember=form.remember.data)
            flash('Login realizado com sucesso.', 'success')

            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)

            return redirect(url_for('admin.index'))

        else:
            flash('Falha no login. Verifique seu email e senha.', 'error')

    for k, v in form.errors.items():
        for error in v:
            flash(error, category='warning')

    return render_template('user/login.html', form=form)


@users.route('/logout')
@auth.login_required
def logout():
    auth.logout_user()
    return redirect(url_for('users.login'))


@users.route('/reset-password/<string:token>', methods=['GET', 'POST'])
def reset_password(token: str):
    """Route to reset a password."""
    if auth.current_user.is_authenticated:
        return redirect(url_for('admin.index'))

    user: User = User.verify_reset_password_token(token)
    if not user:
        flash('Token expirado.', 'error')
        return redirect(url_for('users.login'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = auth.generate_password_hash(form.password.data)
        user.password = hashed_password
        session: Session = db.session
        session.add(user)
        session.commit()

        flash('Senha redefinida com sucesso!', 'success')

        return redirect(url_for('users.login'))

    return render_template('user/reset_password.html', form=form)
