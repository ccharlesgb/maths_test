from string import ascii_uppercase

from maths_app import User, guard
from maths_app import models


def get_user_header(client, username="this"):
    with client.application.app_context():
        user = User.lookup(username)
        header = guard.pack_header_for_user(user)
    return header


def generate_test_question(body, num_options, num_correct, test=None):
    """
    Generate a test question with attached test. Options will simply
    be the uppercase letters of the alphabet with the first 'num_correct' marked as correct

    Limited to 26 options

    :param body: The question body that is being asked
    :type body: str
    :param num_options: The number of options available in the question
    :type num_options: int
    :param num_correct: The number of correct options
    :type num_correct: int
    :param test: The test to attach to
    :type test: models.Test
    :return: The example question object
    :rtype: models.Question
    """
    if num_options > 26:
        raise ValueError("Can't have more than 26 options")
    if num_correct > num_options:
        raise ValueError("can't have more correct options than available options")
    question = models.Question(body=body, test=test)
    for i in range(0, num_options):
        option = models.Option(value=ascii_uppercase[i], correct=i < num_correct)
        question.options.append(option)
    return question
