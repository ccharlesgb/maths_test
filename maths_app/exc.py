from flask import jsonify


class APIError(Exception):
    allowed_categories = {"NOT_FOUND": 404, "INVALID_USAGE": 400}

    def __init__(self, category, message, status_code=None):
        if category not in self.allowed_categories.keys():
            raise ValueError("Unknown API error category '{}'".format(category))
        self.status_code = status_code or self.allowed_categories[category]
        self.message = message
        self.category = category

    @property
    def response_data(self):
        return {"error": self.category, "message": self.message}


def handle_api_error(error):
    return jsonify(error.response_data), error.status_code


def handle_marshmallow_error(error):
    error_data = {"error": "VALIDATION_ERROR", "messages": error.messages}
    return jsonify(error_data), 400
