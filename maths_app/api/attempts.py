from flask import request, jsonify
from flask_praetorian import auth_required, current_user, current_rolenames
from sqlalchemy.orm import exc as orm_exc

from maths_app import models, exc
from maths_app.models import db
from . import api, restricted, student_only
from .common import check_test_id_visible, is_student
from datetime import datetime


@api.route("/tests/<test_id>/attempts", methods=["POST"])
@student_only
def start_attempt(test_id):
    check_test_id_visible(test_id, raise_exc=True)
    # Not expecting a body here just starting a new attempt
    new_attempt = models.Attempt(test_id=test_id, user_id=current_user().id, started_utc=datetime.utcnow())

    db.session.add(new_attempt)
    db.session.commit()

    return jsonify({"message": "New attempt started", "id": new_attempt.id}), 201


def _get_attempt_rows(test_id, attempt_id=None):
    check_test_id_visible(test_id, raise_exc=True)

    attempt_query = models.Attempt.query.filter_by(test_id=test_id)
    # If we are a student we can only see attempts by ourselves. Otherwise
    if is_student():
        attempt_query = attempt_query.filter_by(user_id=current_user().id)
    if attempt_id:
        attempt_query = attempt_query.filter_by(id=attempt_id)
    return attempt_query.all()


@api.route("/tests/<test_id>/attempts", methods=["GET"])
@auth_required
def get_all_attempts(test_id):
    attempt_rows = _get_attempt_rows(test_id)
    attempts = models.AttemptSchema(many=True).load(attempt_rows)
    return jsonify(attempts), 200


@api.route("/tests/<test_id>/attempts/<attempt_id>", methods=["GET"])
@auth_required
def get_attempt(test_id, attempt_id):
    attempt_row = _get_attempt_rows(test_id, attempt_id)
    if not attempt_row:  # Empty list
        raise exc.APIError("NOT_FOUND", "Could not find attempt with test_id={} and attempt_id={}. "
                                        "It either does not exist or"
                                        " you do not have permission to view it".format(test_id, attempt_id))

    attempt = models.AttemptSchema().load(attempt_row[0])
    return jsonify(attempt), 200
