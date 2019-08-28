from flask import Blueprint, request, jsonify
from maths_app import guard, utils, models
from maths_app.models import db
from flask_praetorian import auth_required, current_user, roles_required, roles_accepted
from sqlalchemy.orm import exc as orm_exc

api = Blueprint("api", __name__, url_prefix="/api")

restricted = roles_accepted("admin", "teacher")


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


@api.route("/test/<id>", methods=["GET"])
@auth_required
def get_test(id):
    test_row = db.Test.query.filter_by(id=id).one_or_none()
    if test_row is None:
        return jsonify({"error": "NOT_FOUND", "message": "Could not find test with id={}".format(id)}), 404
    return models.TestSchema().dump(test_row)


@api.route("/test", methods=["POST"])
@restricted
def add_test():
    req_data = request.get_json(force=True)
    new_test = models.TestSchema().load(req_data)
    db.session.add(new_test)
    db.session.commit()
    return jsonify({"message": "New user created", "id": new_test.id}), 201


@api.route("/test/<id>", methods=["PATCH"])
@restricted
def toggle_test_enabled(id):
    try:
        test = models.Test.query.filter_by(id=id).one()
    except orm_exc.NoResultFound as e:
        return jsonify({"error": "NOT_FOUND", "message": "No test found with id={}".format(id)}), 404
    test.enabled = not test.enabled
    db.session.commit()

    new_state = "enabled" if test.enabled else "disabled"
    return jsonify({"message": "The test was {}".format(new_state), "id": id}), 200


@api.route("/test/<test_id>/question", methods=["POST"])
@restricted
def add_question(test_id):
    try:
        test = models.Test.query.filter_by(id=test_id).one()
    except orm_exc.NoResultFound as e:
        return jsonify({"error": "NOT_FOUND", "message": "No test found with id={}".format(test_id)}), 404
    req_data = request.get_json(force=True)
    new_question = models.QuestionSchema().load(req_data)
    new_question.test = test
    models.db.session.add(new_question)
    models.db.session.commit()

    return jsonify({"message": "Neq question created", "id": new_question.id}), 201


@api.route("/test/<test_id>/question/<question_id>", methods=["GET"])
@auth_required
def get_question(test_id, question_id):
    # TODO: Probably more natural to migrate to a question number here instead of the raw DB id?
    try:
        question = models.Question.query.filter_by(test_id=test_id, id=question_id).one()
    except orm_exc.NoResultFound as e:
        return jsonify({"error": "NOT_FOUND",
                        "message": "No question in test={} found with id={}".format(test_id, question_id)}), 404
    print(current_user().rolenames)

    # Student's can't see disabled tests only teachers/admins
    if current_user().rolenames == ["student"] and not question.test.enabled:
        return jsonify({"error": "NOT_FOUND", "message": "No test found with id={}".format(test_id)}), 404

    question_data = models.QuestionSchema().dump(question)
    return jsonify(question_data), 200
