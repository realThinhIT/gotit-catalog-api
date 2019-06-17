import json
import itertools
from tests.helpers import create_headers, json_response


def test_post_login_correct_credentials(client):
    credential = {
        'username': 'thinhnd',
        'password': '1234567'
    }

    response = client.post(
        '/authentication',
        headers=create_headers(),
        data=json.dumps(credential)
    )

    # Check if server returns 200
    assert response.status_code == 200

    # Check if the server return an access_token
    assert 'access_token' in json_response(response).keys()


def test_post_login_invalid_credentials(client):
    credential = {
        'username': '_thinhnd',
        'password': '1234567'
    }

    response = client.post(
        '/authentication',
        headers=create_headers(),
        data=json.dumps(credential)
    )

    # Check if server returns 401
    assert response.status_code == 401

    # Check if these keys exists in response
    assert all(
        key in json_response(response).keys()
        for key in ['message', 'error_code']
    ) is True


def test_post_login_invalid_input(client):
    combine_data = {
        'username': [None, '', 1234, 'thinh nguyen', 'with/specialchars'],
        'password': [None, '', '123456']
    }

    combinations = itertools.product(*combine_data.values())

    num_valid_combine = 0
    for combination in combinations:
        data = dict((k, v) for k, v in zip(combine_data.keys(), combination))
        print(data)
        response = client.post(
            '/authentication',
            data=data
        )

        num_valid_combine += 1 if response.status_code != 400 else 0

        # Check if valid combination counter always equals to 0 (all cases are invalid)
        assert num_valid_combine <= 1


def test_post_register_correct_input(client):
    credential = {
        'username': 'thinhnd3',
        'password': '1234567',
        'name': 'Thinh Nguyen',
        'email': 'thinhnd.ict3@gmail.com'
    }

    response = client.post(
        '/users',
        headers=create_headers(),
        data=json.dumps(credential)
    )

    resp = json_response(response)

    # Check if server returns 200
    assert response.status_code == 200

    # Check if these keys exists in response
    assert all(
        key in resp
        for key in ['id', 'username', 'name', 'created', 'updated']
    ) is True

    # Check if password not in response
    assert 'password' not in resp.keys()


def test_post_register_duplicated_user(client):
    credential = {
        'username': 'thinhnd',
        'password': '1234567',
        'name': 'Thinh Nguyen',
        'email': 'thinhnd.ict@gmail.com'
    }

    response = client.post(
        '/users',
        headers=create_headers(),
        data=json.dumps(credential)
    )

    resp = json_response(response)

    # Check if server returns 400
    assert response.status_code == 400

    # Check if these keys exists in response
    assert all(
        key in resp
        for key in ['error_code', 'message']
    ) is True


def test_post_register_invalid_input(client):
    combine_data = {
        'username': [None, '', 1234, 'thinh nguyen', 'with/specialchars'],
        'email': [None, '', 'not an email', 'test@gmail.com'],
        'password': [None, '', '12345']
    }

    combinations = itertools.product(*combine_data.values())

    num_valid_combine = 0
    for combination in combinations:
        data = dict((k, v) for k, v in zip(combine_data.keys(), combination))
        response = client.post(
            '/users',
            data=data
        )

        num_valid_combine += 1 if response.status_code != 400 else 0

        # Check if valid combination counter always equals to 0 (all cases are invalid)
        assert num_valid_combine <= 1
