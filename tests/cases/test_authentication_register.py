import json
import itertools
from tests.helpers import create_headers, json_response


def test_post_correct_input(client):
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


def test_post_invalid_json(client):
    response = client.post(
        '/users',
        headers=create_headers(),
        data="{"
    )

    # Check if server returns 400
    assert response.status_code == 400


def test_post_duplicated_username(client):
    credential = {
        'username': 'thinhnd',
        'password': '1234567',
        'name': 'Thinh Nguyen',
        'email': 'thinhnd.ict2222@gmail.com'
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


def test_post_duplicated_email(client):
    credential = {
        'username': 'thinhnd222',
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


def test_post_invalid_input(client):
    combine_data = {
        'username': [None, '', 1234, 'thinh nguyen', 'with/specialchars', 'thinhndvalidate', 'invalid_input*'],
        'email': [None, '', 'not an email', 'test@gmail.com'],
        'password': [None, '', '12345', '123456'],
        'name': [None, '1234', '']
    }

    # To create combinations of 4
    combinations = itertools.product(*combine_data.values())

    num_valid_combine = 0
    for combination in combinations:
        # Map key -> value of tuples
        data = dict((k, v) for k, v in zip(combine_data.keys(), combination))
        response = client.post(
            '/users',
            data=data
        )

        num_valid_combine += 1 if response.status_code != 400 else 0

        # Check if valid combination counter always equals to 0 (all cases are invalid)
        assert num_valid_combine <= 1


def test_post_invalid_username(client):
    credential = {
        'username': 'thinhnd222*',
        'password': '1234567',
        'name': 'Thinh Nguyen',
        'email': 'thinhnd.ict11111@gmail.com'
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
