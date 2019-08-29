from flask import request, jsonify
from flask_praetorian import auth_required, current_user, current_rolenames
from sqlalchemy.orm import exc as orm_exc

from maths_app import models, exc
from maths_app.models import db
from . import api, restricted
from .common import check_test_visible


@api.route("/tests/<id>", methods=["GET"])
@auth_required
def get_test(id):
    test_row = models.Test.query.filter_by(id=id).one_or_none()
    if test_row is None:
        raise exc.APIError("NOT_FOUND", "Could not find test with id={}".format(id))

    check_test_visible(test_row, raise_exc=True)

    return models.TestSchema().dump(test_row), 200


@api.route("/tests", methods=["POST"])
@restricted
def add_test():
    req_data = request.get_json(force=True)
    new_test = models.TestSchema().load(req_data)
    db.session.add(new_test)
    db.session.commit()
    return jsonify({"message": "New user created", "id": new_test.id}), 201


@api.route("/tests", methods=["GET"])
@restricted
def get_all_tests():
    test_rows = models.Test.query.all()
    test_rows = filter(check_test_visible, test_rows)

    return jsonify(models.TestSchema(many=True).dump(test_rows)), 200


@api.route("/tests/<id>", methods=["PATCH"])
@restricted
def toggle_test_enabled(id):
    try:
        test = models.Test.query.filter_by(id=id).one()
    except orm_exc.NoResultFound as e:
        raise exc.APIError("NOT_FOUND", "Could not find test with id={}".format(id))
    test.enabled = not test.enabled
    db.session.commit()

    new_state = "enabled" if test.enabled else "disabled"
    return jsonify({"message": "The test was {}".format(new_state), "id": id}), 200


@api.route("/tests/<test_id>/questions", methods=["POST"])
@restricted
def add_question(test_id):
    try:
        test = models.Test.query.filter_by(id=test_id).one()
    except orm_exc.NoResultFound as e:
        raise exc.APIError("NOT_FOUND", "Could not find test with id={}".format(id))
    req_data = request.get_json(force=True)
    new_question = models.QuestionSchema().load(req_data)
    new_question.test = test
    models.db.session.add(new_question)
    models.db.session.commit()

    return jsonify({"message": "New question created", "id": new_question.id}), 201


@api.route("/tests/<test_id>/questions/<question_id>", methods=["GET"])
@auth_required
def get_question(test_id, question_id):
    try:
        question = models.Question.query.filter_by(test_id=test_id, id=question_id).one()
    except orm_exc.NoResultFound as e:
        raise exc.APIError("NOT_FOUND", "No question in test={} found with id={}".format(test_id, question_id))

    check_test_visible(question.test, raise_exc=True)

    question_data = models.QuestionSchema().dump(question)
    return jsonify(question_data), 200
