from flask import request, jsonify
from flask_praetorian import auth_required, current_user

from maths_app import guard, utils, models
from maths_app.models import db
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
