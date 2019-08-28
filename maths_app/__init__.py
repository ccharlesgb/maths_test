from flask import Flask
import os


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

    return app
