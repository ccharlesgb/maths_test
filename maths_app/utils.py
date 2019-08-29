import os

from .models import db, guard, User, Role

DEFAULT_ROLES = ["admin", "teacher", "student"]


def get_role(name):
    return Role.query.filter_by(name=name).one()


def init_db():
    """
    Create all the tables for the application
    Create the roles required for the application
    Create the default admin user (In prod use environment to get admin password)

    Can only be run in app context

    :return:
    """
    db.drop_all()
    db.create_all()
    roles = [Role(name=elem) for elem in DEFAULT_ROLES]
    db.session.add_all(roles)
    db.session.commit()

    create_user("admin", os.environ.get("APP_ADMIN_PASS", "admin"), "admin", "Admin")
    # TODO: Testing purposes only so the app has some defalut users to play with
    create_user("teacher", "teacher1", "teacher", "Teacher 1")
    create_user("student", "student1", "student", "Student 1")


def create_user(username, password, rolename, full_name, email=None):
    """
    Utility function for creating a user and hashing the password

    Can only be run in app context

    :param username:
    :param password:
    :param rolename:
    :param full_name:
    :param email:
    :return:
    """
    pass_hash = guard.hash_password(password)
    admin_user = User(username=username, password=pass_hash, role=get_role(rolename), full_name=full_name, email=email)
    db.session.add(admin_user)
    db.session.commit()
