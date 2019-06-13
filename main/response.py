from flask import make_response, json


class SuccessResponse(object):
    @staticmethod
    def output_json(data, code=200, message='Action performed successfully', additional_data=None, headers=None):
        """
        To manipulate structure of response payload.

        :param data:
        :param code:
        :param message:
        :param additional_data:
        :param headers:
        :return: flask.Response instance
        """
        if code in [200, 201]:
            prepared_data = {
                'success': 1,
                'message': message,
                'data': data,
                'additional_data': additional_data
            }
        else:
            prepared_data = data

        resp = make_response(json.dumps(prepared_data), code)
        resp.headers.extend(headers or {})
        return resp
