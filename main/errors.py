from flask import jsonify
from marshmallow import fields, Schema


class ErrorSchema(Schema):
    error_code = fields.Int()
    message = fields.String()
    errors = fields.Raw()


class Error(Exception):
    """
    This is the base class for Flask Exceptions,
    To give basic structure to error payload.
    """

    status_code = 500

    def __init__(self, errors={}):
        super(Error)
        self.errors = errors or {}

    def to_response(self):
        resp = jsonify(ErrorSchema().dump(self).data)
        resp.status_code = self.status_code
        return resp


class StatusCode(object):
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    INTERNAL_SERVER_ERROR = 500


class ErrorCode(object):
    BAD_REQUEST = 40000
    VALIDATION_ERROR = 40001
    ALREADY_EXISTS = 40002
    DOES_NOT_EXIST = 40003
    WRONG_CONTENT_TYPE = 40004
    INVALID_RESOURCE = 40005
    INVALID_PAGINATION_FORMAT = 40006
    PAGE_EXCEEDED_RANGE = 40007                     # If user request a page larger than total pages
    UNAUTHORIZED = 40100
    NOT_FOUND = 40400
    INTERNAL_SERVER_ERROR = 50000
    FORBIDDEN = 40300

    # CATEGORY
    CATEGORY_NOT_FOUND = 40401


class InternalServerError(Error):
    status_code = StatusCode.INTERNAL_SERVER_ERROR
    error_code = ErrorCode.INTERNAL_SERVER_ERROR
    message = 'There was a problem processing your request.'


class NotFoundError(Error):
    status_code = StatusCode.NOT_FOUND
    error_code = ErrorCode.NOT_FOUND
    message = 'The resource requested doesn\'t exist.'


class NotFoundError(Error):
    status_code = StatusCode.NOT_FOUND
    error_code = ErrorCode.NOT_FOUND
    message = 'The resource requested doesn\'t exist.'


class CategoryNotFoundError(Error):
    status_code = StatusCode.NOT_FOUND
    error_code = ErrorCode.CATEGORY_NOT_FOUND
    message = 'The category requested doesn\'t exist.'


class BadRequestError(Error):
    status_code = StatusCode.BAD_REQUEST
    error_code = ErrorCode.BAD_REQUEST
    message = 'Bad request, please try again.'


class InvalidPaginationFormatError(Error):
    status_code = StatusCode.BAD_REQUEST
    error_code = ErrorCode.INVALID_PAGINATION_FORMAT
    message = 'Information provided for pagination is not in a valid format.'


class ExceededRangePaginationError(Error):
    status_code = StatusCode.BAD_REQUEST
    error_code = ErrorCode.PAGE_EXCEEDED_RANGE
    message = 'The page you requested exceeds the max range of total pages.'


class WrongContentTypeError(Error):
    status_code = StatusCode.BAD_REQUEST
    error_code = ErrorCode.WRONG_CONTENT_TYPE
    message = 'The payload sent to server is not a valid JSON. Please try again.'


class InputValidationError(Error):
    status_code = StatusCode.BAD_REQUEST
    error_code = ErrorCode.VALIDATION_ERROR
    message = 'Some inputs are invalid, please correct and try again.'


class DuplicatedResourceError(Error):
    status_code = StatusCode.BAD_REQUEST
    error_code = ErrorCode.ALREADY_EXISTS
    message = 'The resource you trying to modify already exists.'


class ForbiddenError(Error):
    status_code = StatusCode.FORBIDDEN
    error_code = ErrorCode.FORBIDDEN
    message = 'You don\'t have the rights to access and modify this resource.'


class InvalidCredentialsError(Error):
    status_code = StatusCode.UNAUTHORIZED
    error_code = ErrorCode.UNAUTHORIZED
    message = 'Invalid credentials. Username and/ or password is not correct. Please check and try again.'


class UnauthorizedError(Error):
    status_code = StatusCode.UNAUTHORIZED
    error_code = ErrorCode.UNAUTHORIZED
    message = 'Invalid credentials. Please provide a valid access token.'

