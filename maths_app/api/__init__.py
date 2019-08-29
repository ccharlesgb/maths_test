# flake8: noqa
from flask import Blueprint
from flask_praetorian import roles_accepted

api = Blueprint("api", __name__, url_prefix="/api")
restricted = roles_accepted("admin", "teacher")

from .users import *
from .tests import *
