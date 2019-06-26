import functools

from flask import request
from marshmallow import ValidationError

from main.errors import WrongContentTypeError, InputValidationError


# Validate JSON payload sent to the server using corresponding schema.
# Raise InputValidationError if the payload doesn't meet schema definitions.
def parse_with_schema(schema=None):
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
            kwargs['data'] = data
            return func(*args, **kwargs)
        return func_with_decorator
    return decorator
