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
