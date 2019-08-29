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
    return ["student"] in current_rolenames()
