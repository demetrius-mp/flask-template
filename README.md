# flask-template

Starter template for Flask applications using the factory pattern. Feel free to 
open pull requests, issues, or leaving any suggestions!

## What it includes
- [Bootstrap 5.0.2](https://github.com/twbs/bootstrap/releases/tag/v5.0.2).
- [Bootstrap Icons 1.6.0](https://github.com/twbs/icons/releases/tag/v1.6.0).
- [jQuery 3.6.0](https://github.com/jquery/jquery/releases/tag/3.6.0).
- [toastr 2.1.1](https://github.com/CodeSeven/toastr/releases/tag/2.1.1).
- [Roboto font](https://fonts.google.com/specimen/Roboto).

## Extensions
- Login manager - [Flask-Login](https://github.com/maxcountryman/flask-login).
- Database - [Flask-SQLAlchemy](https://github.com/pallets/flask-sqlalchemy/).
- Database migrations - [Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate)
- Environment configuration - [Dynaconf](https://github.com/rochacbruno/dynaconf).
- Translation support - [Flask-BabelEx](https://github.com/mrjoes/flask-babelex). **[See this issue](https://github.com/demetrius-mp/flask-template/issues/2).**
- Admin panel - [Flask-Admin](https://github.com/flask-admin/flask-admin).

## Built-in stuff
- Login system with password encryption.
- Login page.
- Password reset system with timed tokens.
- Password reset page.
- Users management on the admin panel.

## Stuff you might want to know
- All flashed messages are flashed as a toast notification.

## How to customize

### Adding extensions
Create a new file under `application/extensions/{filename}.py`. This file
can't have the same name as the extension.

Instantiate the extension and add and `init_app` function, that receives a Flask app instance.
Example below using Flask-SQLAlchemy extension:
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app: Flask):
    db.init_app(app)
```

If you want to put the extension in a package, the `init_app` function should be in the
`__init__.py` file.

To load the extension in the application, open the `settings.toml` file, and add 
the extension to the extensions list as below:
```
EXTENSIONS = [
    ...
    "application.extensions.{filename}:init_app",
    ...
]
```

You must pay attention to the order that your extensions are loaded, if any order is
required.

### Adding blueprints
Create a new package under `application/blueprints/{blueprint_name}/`.
Create a `routes.py` file, where the blueprint will be instantiated. 

#### Adding templates to a blueprint

If you are willing to store templates in this blueprint, add the parameter 
`templates_folder='templates'` when instantiating the blueprint.
Also, you must place your templates in the following directory:
`applications/blueprints/{blueprint_name}/templates/{blueprint_name}/`.
Yes, you must create another folder inside the templates folder. This is 
[recommended](https://flask.palletsprojects.com/en/2.0.x/blueprints/#templates)
to avoid getting a template overridden by a template with the same name
in the actual application templates folder.

Example below (without templates):
```python
from flask import Blueprint, render_template

blueprint_name = Blueprint('blueprint_name', __name__)


@blueprint_name.route('/')
def index():
    return render_template('index.html')
```

Example below (with templates):
```python
from flask import Blueprint, render_template

blueprint_name = Blueprint('blueprint_name', __name__, template_folder='templates')


@blueprint_name.route('/')
def index():
    # the template name is blueprint_name/template.html
    return render_template('blueprint_name/index.html')
```

You can create a `forms.py` if you want to user forms in this blueprint.

To register the blueprint to the application, create a `__init__.py` file, 
import the blueprint, and create a `init_app` function that receives a Flask app
intance and register the blueprint. Example below:

```python
from flask import Flask

from application.blueprints.blueprint_name.routes import blueprint_name


def init_app(app: Flask):
    app.register_blueprint(blueprint_name)
```

And finally, to load the blueprint into your application, open the `settings.toml` file
and add the blueprint to the extensions list as below:
```
EXTENSIONS = [
    ...
    "application.blueprints.{blueprint_name}:init_app",
    ...
]
```

Usually, blueprints are loaded after every extension is loaded.

### Adding models

Create a file under `applications/models/{model_name}.py` and import the `db`
object from the `application/extensions/database.py` to declare your model.
Example below:
```python
from application.extensions.database import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(512), nullable=False)
    is_active = db.Column(db.Boolean, default=False)
```

Import the model inside the `application/models/__init__.py` file. Example below:
```python
from application.models.user import User
```

Now your model is accessible from `application.models`

#### Note:
If you need to import a model to use on another model 
(usually happens when creating many-to-many relations, and you need the association table)
import it directly from the model file, not from `application.models`. 
Example below:

```python
# application/models/follow.py

from application.extensions.database import db

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)

"""=============================================================="""

# application/models/user.py

from application.extensions.database import db
# from application.models import followers !!!WRONG!!!
from application.models.follow import followers  # correct

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ...
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers'),
        lazy='dynamic'
    )
    ...
```

If you import from the package instead of file, you will fall into 
circular import.
