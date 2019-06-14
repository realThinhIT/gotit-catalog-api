import functools
from flask import request
from marshmallow import ValidationError
from main.errors import WrongContentTypeError, InputValidationError, InvalidPaginationFormatError
from main.schemas.pagination import RequestPaginationSchema
from main.utils.pagination import PaginationUtils


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
            kwargs['data'] = data
            return func(*args, **kwargs)
        return func_with_decorator
    return decorator


def parse_with_pagination(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        # Get query strings from the request
        rargs = request.args

        # Validate pagination
        try:
            pagination = RequestPaginationSchema().load(rargs)
            pagination = PaginationUtils.calc_pagination(pagination.get('page'), pagination.get('per_page'))

            kwargs['pagination'] = pagination
        except ValidationError, err:
            raise InvalidPaginationFormatError(err.messages)

        return func(*args, **kwargs)
    return decorator
