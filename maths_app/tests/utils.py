from maths_app import User, guard


def get_user_header(client, username="this"):
    with client.application.app_context():
        user = User.lookup(username)
        header = guard.pack_header_for_user(user)
    return header
