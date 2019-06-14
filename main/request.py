import functools
from flask import request
from marshmallow import ValidationError
from main.errors import WrongContentTypeError, InputValidationError


def validate_with_schema(schema=None):
    def decorator(func):
        @functools.wraps(func)
        def func_with_decorator(*args, **kwargs):
            # Try to parse JSON from payload
            try:
                data = request.get_json() or {}
            except Exception:
                raise WrongContentTypeError()

            # Try to validate the object
            # If the payload is invalid, throw an error message
            try:
                schema.load(data)
            except ValidationError, err:
                raise InputValidationError(err.messages)

            # If everything is okay, pass to the function
            return func(data, *args, **kwargs)
        return func_with_decorator
    return decorator
