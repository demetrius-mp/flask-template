from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous.exc import SignatureExpired

from application.extensions.database import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(512), nullable=False)
    is_active = db.Column(db.Boolean, default=False)

    role = db.relationship('Role', back_populates='users')

    def get_reset_password_token(self, expires_sec=600):
        """Generates a timed valid reset password token.

        :param expires_sec: amount of the time that the token will be valid, in seconds. Defaults to 600.
        :return: the token.
        """
        s = Serializer(current_app.secret_key, expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token: str):
        """Verifies the token, and, if it is valid and not expired, returns the user.

        :param token: the token to be verified.
        :return: the user associated.
        """
        s = Serializer(current_app.secret_key)
        try:
            user_id = s.loads(token)['user_id']
        except SignatureExpired:
            return None

        return User.query.get(user_id)

    def __repr__(self):
        return self.full_name
