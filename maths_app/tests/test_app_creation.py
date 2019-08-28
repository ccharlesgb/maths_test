from maths_app import create_app


def test_app_creation_dict():
    env_config = {"TEST_KEY1": "TEST_VALUE1", "TEST_KEY2": "TEST_VALUE2"}
    app = create_app(env_config)
    for key_name, value in env_config.items():
        assert app.config[key_name] == value
