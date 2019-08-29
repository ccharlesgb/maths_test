from flask_praetorian import auth_required, current_user, current_rolenames
from maths_app import models, exc


def check_test_visible(test, raise_exc=False):
    # Student's can't see disabled tests only teachers/admins
    visible = "student" not in current_rolenames() or test.enabled
    if not visible and raise_exc:
        raise exc.APIError("NOT_FOUND", "Could not find test with id={}".format(id))

    return visible


def check_test_id_visible(test_id, raise_exc=False):
    test = models.Test.query.filter_by(id=test_id).one_or_none()
    if not test:
        if raise_exc:
            raise exc.APIError("NOT_FOUND", "Could not find test with id={}".format(id))
        else:
            return False
    return check_test_visible(test, raise_exc)


def is_student():
    return "student" in current_rolenames()


def check_user_is_attempting(test_id, raise_exc=False):
    user_id = current_user().id
    attempt = models.Attempt.query.filter_by(user_id=user_id, test_id=test_id)
    attempt = attempt.filter(models.Attempt.completed_utc == None)  # noqa
    attempting = attempt.one_or_none() is not None

    if not attempting and raise_exc:
        raise exc.APIError("INVALID_USAGE", "Can't perform this operation on test={} as you are "
                                            "not currently attempting it".format(test_id))

    return attempting


def get_test_question_count(test_id):
    return models.Question.query.filter_by(test_id=test_id).count()
