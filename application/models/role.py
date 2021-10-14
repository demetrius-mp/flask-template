from application.extensions.database import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(512))

    users = db.relationship('User', back_populates='role')

    def __repr__(self):
        return self.name
