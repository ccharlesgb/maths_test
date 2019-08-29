import click
from flask.cli import FlaskGroup

from . import create_app
from .utils import init_db


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    pass


@cli.command()
def initdb():
    """
    Initialise the database. Should only be run once to bootstrap the application

    1. Creates the database tables
    2. Creates the 3 roles defined in project spec
    3. Creates the first user 'admin' to allow administration
    """
    init_db()
