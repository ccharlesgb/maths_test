from flask import Blueprint, request, jsonify
from maths_app import guard

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/login", methods=["POST"])
def login():
    """
    Login route. Expects json body with 'username' and 'password'

    :return: JSON response with the JWT token to authenticate further requests
    """
    req_data = request.get_json(force=True)
    user = guard.authenticate(req_data.get("username"), req_data.get("password"))
    return jsonify({"token": guard.encode_jwt_token(user)})
