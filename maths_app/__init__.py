from flask import Flask
import os
from .models import db, guard, ma, User
from .api import api
from . import exc


class Defaults:
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = "jdj239adka0ak"  # Change for prod


def create_app(dict_config=None):
    app = Flask(__name__)
    # Initialise with default settings and then override with specified config
    app.config.from_object(Defaults)

    if dict_config:
        app.config.from_mapping(dict_config)
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["APP_DATABASE"]
        app.config["SECRET_KEY"] = os.environ["APP_SECRET"]

    app.register_blueprint(api)
    app.errorhandler(exc.APIError)(exc.handle_api_error)

    db.init_app(app)
    ma.init_app(app)
    guard.init_app(app, User)

    return app
