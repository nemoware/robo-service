from functools import wraps

import jsonschema
from flask import request, jsonify
from jsonschema import Draft7Validator


def validate_schema(schema):
    validator = Draft7Validator(schema, format_checker=jsonschema.FormatChecker())

    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            input = request.get_json(force=True)
            errors = [error.message for error in validator.iter_errors(input)]
            if errors:
                response = jsonify(dict(message="invalid input", errors=errors))
                response.status_code = 406
                return response
            else:
                return fn(*args, **kwargs)
        return wrapped
    return wrapper