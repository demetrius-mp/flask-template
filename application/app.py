from application import flask_app


def create_app():
    flask_application = flask_app.create_app()

    return flask_application
