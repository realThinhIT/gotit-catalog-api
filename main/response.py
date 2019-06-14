from flask import make_response, json, jsonify, Response
import functools


class Response(object):
    @staticmethod
    def output_exception_json(exception=None):
        """
        To manipulate structure of response payload.

        :param exception: Exception instance for errors
        :return: flask.Response instance
        """

        prepared_data = {
            'error_code': exception.error_code,
            'message': exception.message
        }

        if exception.errors != {}:
            prepared_data['errors'] = exception.errors

        resp = make_response(json.dumps(prepared_data), exception.status_code)
        resp.headers.extend({
            'Content-Type': 'application/json'
        })

        return resp


def json_response(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        # Try to parse response to JSON
        func_response = func(*args, **kwargs)

        # Parse data
        is_res = isinstance(func_response, tuple) or isinstance(func_response, Response)
        data = func_response[0] if is_res else func_response
        status_code = func_response[1] if is_res else 200

        # Make response
        try:
            return (
                jsonify(data),
                status_code
            )

        # In case the request was jsonify-ed
        except TypeError:
            return data, status_code

    return decorator
