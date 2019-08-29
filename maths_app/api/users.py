from flask import request, jsonify
from flask_praetorian import auth_required, current_user
from flask_praetorian import roles_required
from sqlalchemy.orm.exc import NoResultFound

from maths_app import utils, models, exc
from maths_app.models import db, guard
from . import api


@api.route("/login", methods=["POST"])
def login():
    """
    Login route. Expects json body with 'username' and 'password'

    :return: JSON response with the JWT token to authenticate further requests
    """
    req_data = request.get_json(force=True)
    user = guard.authenticate(req_data.get("username"), req_data.get("password"))
    return jsonify({"token": guard.encode_jwt_token(user)}), 201


@api.route("/current_user", methods=["GET"])
@auth_required
def current_username():
    cur_user = current_user()
    resp = {"username": cur_user.username, "fullname": cur_user.full_name}
    return resp, 200


@api.route("/register", methods=["POST"])
def register_user():
    req_data = request.get_json(force=True)
    # Pop password hash out before we marshal this as we need to hash it
    password = req_data.pop("password")
    new_user = models.UserSchema().load(req_data)
    new_user.password = guard.hash_password(password)
    new_user.role = utils.get_role("student")  # Only students can register
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "New user created", "id": new_user.id}), 201


@api.route("/users/<id>", methods=["PATCH"])
@roles_required("admin")
def promote_user(id):
    req_data = request.get_json(force=True)
    if not req_data["role"]:
        raise exc.APIError("INVALID_USAGE", "'role' key not supplied")
    try:
        role = utils.get_role(req_data["role"])
    except NoResultFound as e:
        raise exc.APIError("NOT_FOUND", "Could not find role '{}'".format(req_data["role"]))

    user = models.User.query.get(id)
    user.role = role
    db.session.commit()

    return {"message": "User successfully promoted", "id": user.id}
