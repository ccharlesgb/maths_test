from flask_sqlalchemy import SQLAlchemy
from flask_praetorian import Praetorian
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()
guard = Praetorian()
