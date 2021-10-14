from pathlib import Path

import click
from flask import Flask

from application.extensions.auth import generate_password_hash
from application.extensions.database import db
from application.models import User, Role


class BlueprintManager:
    def __init__(self, name: str, with_templates: bool = False, with_forms: bool = False):
        self.name = name
        self.blueprint_path = Path.cwd() / 'application' / 'blueprints' / self.name
        self.with_templates = with_templates
        self.with_forms = with_forms

        self.blueprint_path.mkdir()

    def create_init(self):
        with open(self.blueprint_path / '__init__.py', 'w') as f:
            content = f"""
from flask import Flask

from application.blueprints.{self.name}.routes import {self.name}


def init_app(app: Flask):
    app.register_blueprint({self.name})

""".lstrip()

            f.write(content)

    def create_template(self):
        templates_path = (self.blueprint_path / 'templates' / self.name)
        templates_path.mkdir(parents=True)

        with open(self.blueprint_path / 'templates' / '.gitkeep', 'w') as f:
            f.write('ignore this file')

        with open(templates_path / 'index.html', 'w') as f:
            f.write('Write your template here.')

    def create_form(self):
        with open(self.blueprint_path / 'forms.py', 'w') as f:
            content = '''
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class FormName(FlaskForm):
    """Form to ..."""
    field1 = StringField('Field One', validators=[DataRequired()])
    submit = SubmitField('Submit')

'''.lstrip()

            f.write(content)

    def create_routes(self):
        with open(self.blueprint_path / 'routes.py', 'w') as f:
            content = f'''
from flask import Blueprint, flash, redirect, url_for, request, render_template

{f'from application.blueprints.{self.name} import forms' if self.with_forms else ""}
from application.extensions import auth
from application.extensions.database import db
from application import models

{self.name} = Blueprint('{self.name}', __name__{", template_folder='templates'" if self.with_templates else ""})


@{self.name}.route("/")
def index():
    """Route to ..."""
    return render_template('{self.name}/index.html')

'''.lstrip()

            f.write(content)

    def create_blueprint(self):
        self.create_init()

        if self.with_templates:
            self.create_template()

        if self.with_forms:
            self.create_form()

        self.create_routes()


def add_blueprint_(name: str, with_templates: bool = False, with_forms: bool = False):
    bp_mgr = BlueprintManager(name, with_templates, with_forms)
    bp_mgr.create_blueprint()


def add_blueprint_1(name: str, with_templates: bool = False, with_forms: bool = False):
    blueprint_path = Path.cwd() / 'application' / 'blueprints' / name

    blueprint_path.mkdir()
    with open(blueprint_path / '__init__.py', 'w') as f:
        content = f"""
from flask import Flask

from application.blueprints.{name}.routes import {name}


def init_app(app: Flask):
    app.register_blueprint({name})

""".lstrip()

        f.write(content)

    if with_templates:
        (blueprint_path / 'templates' / name).mkdir(parents=True)
        with open(blueprint_path / 'templates' / '.gitkeep', 'w') as f:
            f.write('ignore this file')

    if with_forms:
        with open(blueprint_path / 'forms.py', 'w') as f:
            content = '''
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class FormName(FlaskForm):
    """Form to ..."""
    field1 = StringField('Field One', validators=[DataRequired()])
    submit = SubmitField('Submit')

'''.lstrip()

            f.write(content)

    with open(blueprint_path / 'routes.py', 'w') as f:
        content = f'''
from flask import Blueprint, flash, redirect, url_for, request, render_template

{f'from application.blueprints.{name} import forms' if with_forms else ""}
from application.extensions import auth
from application.extensions.database import db
from application import models

users = Blueprint('users', __name__{", template_folder='templates'" if with_templates else ""})


@users.route("/")
def index():
    """Route to ..."""
    return 'Index'

'''.lstrip()

        f.write(content)

    click.echo('Blueprint created successfully!')


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

    @app.cli.command()
    @click.option('--name', '-n', type=click.STRING, required=True)
    @click.option('--with-templates', '-t', type=click.BOOL, default=False)
    @click.option('--with-forms', '-f', type=click.BOOL, default=False)
    def add_blueprint(name: str, with_templates: bool = False, with_forms: bool = False):
        """Adds a blueprint skeleton to the application"""
        add_blueprint_(name, with_templates, with_forms)
