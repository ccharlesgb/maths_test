from flask_marshmallow import Marshmallow
from flask_praetorian import Praetorian
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, validate

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
    email = db.Column(db.String(256), unique=False, nullable=True)

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


class Test(db.Model):
    """
    This model represents a test to be taken
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    pass_fraction = db.Column(db.Float, nullable=False)
    enabled = db.Column(db.Boolean, nullable=False, default=False)


class Question(db.Model):
    """
    This model represents a question inside a test
    Questions can only be a part of a single test.

    TODO: Create mapping table so we can have a bank of questions and create tests from here?
    """
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(128), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey("test.id"), nullable=False)

    test = db.relationship("Test", backref=db.backref("questions"))


class Option(db.Model):
    """
    This model defines an option for the question. Whether the answer is correct is stored here, multiple answers
    can be correct
    """
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    value = db.Column(db.Text, nullable=False)
    correct = db.Column(db.Boolean, nullable=False, default=False)

    question = db.relationship("Question", backref=db.backref("options", lazy="joined"))


class Attempt(db.Model):
    """
    This marks an attempt by a user to take a test. Once they have completed the test you can calculate the
    percentage

    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey("test.id"), nullable=False)
    started_utc = db.Column(db.DateTime, nullable=False)
    completed_utc = db.Column(db.DateTime, nullable=True)
    mark = db.Column(db.Integer, nullable=True)


class Answer(db.Model):
    """
    This marks an individual option chosen by a user for a given attempt
    """
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey("attempt.id"), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey("option.id"), nullable=False)
    chosen_utc = db.Column(db.DateTime, nullable=False)

    attempt = db.relationship("Attempt", backref=db.backref("answers", lazy="joined"))
    option = db.relationship("Option")


"""
Schemas for models

TODO: Think about validation in serializers here
"""


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


class TestSchema(ma.ModelSchema):
    pass_fraction = fields.Float(validate=validate.Range(min=0.0, max=1.0))

    class Meta:
        model = Test


class QuestionSchema(ma.ModelSchema):
    options = fields.Nested("OptionSchema", only=["id", "value", "correct"], many=True)

    class Meta:
        model = Question


class OptionSchema(ma.ModelSchema):
    class Meta:
        model = Option


class AttemptSchema(ma.ModelSchema):
    started_utc = fields.DateTime()

    class Meta:
        # dateformat = '%Y-%m-%dT%H:%M:%S'
        model = Attempt


class AnswerSchema(ma.ModelSchema):
    class Meta:
        model = Answer
