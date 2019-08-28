from flask_sqlalchemy import SQLAlchemy
from flask_praetorian import Praetorian
from flask_marshmallow import Marshmallow
from marshmallow import fields

db = SQLAlchemy()
ma = Marshmallow()
guard = Praetorian()


class User(db.Model):
    """
    This probably deviates slightly from the brief where students "register to take a test"
    but this way I can unify the authentication between teachers and students
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    # TODO: Implement guard email verification
    is_active = db.Column(db.Boolean, default=True, server_default="TRUE")

    # Extra Info
    full_name = db.Column(db.String(256), unique=False, nullable=False)
    email = db.Column(db.String(256), unique=False, nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.filter_by(id=id).one_or_none()

    @property
    def identity(self):
        return self.id

    @property
    def rolenames(self):
        # TODO: Multiple roles? 1->1 mapping here
        return [self.role.name]

    def is_valid(self):
        return self.is_active

    role = db.relationship("Role", lazy="joined")


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)


class UserSchema(ma.ModelSchema):
    role = fields.Nested("RoleSchema", only=["name"])
    email = fields.Email()

    class Meta:
        # Probably would never want to serialise the password hash in the JSON api
        exclude = ("password",)
        model = User


class RoleSchema(ma.ModelSchema):
    class Meta:
        model = Role
