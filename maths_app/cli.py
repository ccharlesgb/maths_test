import click
from flask.cli import FlaskGroup
from . import create_app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    pass
