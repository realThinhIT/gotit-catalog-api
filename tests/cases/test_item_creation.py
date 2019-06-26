import json
import itertools

from tests.creation import _create_user
from tests.helpers import create_headers, json_response, generate_access_token, random_string


def test_post_authorized(client):
    # Init data
    user = _create_user(client)
    headers = create_headers(
        access_token=generate_access_token(user['id'])
    )

    category_id = 1
    data = {
        'name': 'My Item {}'.format(random_string(10))
    }

    # Create item
    response = client.post(
        '/categories/{}/items'.format(category_id),
        headers=headers,
        data=json.dumps(data)
    )

    resp = json_response(response)

    # Check if server returns 200
    assert response.status_code == 200

    # Check if each dict contains these keys
    assert all(
        key in resp
        for key in ['id', 'name', 'description', 'updated', 'created']
    ) is True

    # Check if newly created item is has the same name
    assert resp['name'] == data['name']
    assert resp['description'] == ''


def test_post_authorized_with_description(client):
    # Init data
    user = _create_user(client)
    headers = create_headers(
        access_token=generate_access_token(user['id'])
    )

    category_id = 1
    data = {
        'name': 'My Item {}'.format(random_string(10)),
        'description': '{}'.format(random_string(100))
    }

    # Create item
    response = client.post(
        '/categories/{}/items'.format(category_id),
        headers=headers,
        data=json.dumps(data)
    )

    resp = json_response(response)

    # Check if server returns 200
    assert response.status_code == 200

    # Check if each dict contains these keys
    assert all(
        key in resp
        for key in ['id', 'name', 'description', 'updated', 'created']
    ) is True

    # Check if newly created item is has the same name
    assert resp['name'] == data['name']
    assert resp['description'] == data['description']


def test_post_authorized_unrecognized_field(client):
    # Init data
    user = _create_user(client)
    headers = create_headers(
        access_token=generate_access_token(user['id'])
    )

    category_id = 1
    data = {
        'id': 100,
        'name': 'My Item {}'.format(random_string(10))
    }

    # Create item
    response = client.post(
        '/categories/{}/items'.format(category_id),
        headers=headers,
        data=json.dumps(data)
    )

    resp = json_response(response)

    # Check if server returns 400
    assert response.status_code == 400

    # Check if each dict contains these keys
    assert all(
        key in resp
        for key in ['error_code', 'message']
    ) is True


def test_post_duplicated_content(client):
    # Init data
    user = _create_user(client)
    headers = create_headers(
        access_token=generate_access_token(user['id'])
    )

    category_id = 1
    data = {
        'name': 'My Item {}'.format(random_string(10))
    }

    # Create item
    client.post(
        '/categories/{}/items'.format(category_id),
        headers=headers,
        data=json.dumps(data)
    )

    response2 = client.post(
        '/categories/{}/items'.format(category_id),
        headers=headers,
        data=json.dumps(data)
    )

    resp = json_response(response2)

    # Check if server returns 400
    assert response2.status_code == 400

    # Check if each dict contains these keys
    assert all(
        key in resp
        for key in ['error_code', 'message']
    ) is True


def test_post_authorized_invalid_input(client):
    # Init data
    user = _create_user(client)
    headers = create_headers(
        access_token=generate_access_token(user['id'])
    )

    category_id = 1
    combine_data = {
        'name': [None, '', '{}'.format(random_string(100))],
        'description': [None, '', 'ABC']
    }

    combinations = itertools.product(*combine_data.values())

    num_valid_combine = 0
    for combination in combinations:
        data = dict((k, v) for k, v in zip(combine_data.keys(), combination))

        # Create item
        response = client.post(
            '/categories/{}/items'.format(category_id),
            headers=headers,
            data=json.dumps(data)
        )

        num_valid_combine += 1 if response.status_code != 400 else 0

        # Check if valid combination counter always equals to 0 (all cases are invalid)
        assert num_valid_combine <= 1


def test_post_no_name_field(client):
    # Init data
    user = _create_user(client)
    headers = create_headers(
        access_token=generate_access_token(user['id'])
    )

    category_id = 1
    data = {
        'description': 'Hello testing'
    }

    # Create item
    response = client.post(
        '/categories/{}/items'.format(category_id),
        headers=headers,
        data=json.dumps(data)
    )

    resp = json_response(response)

    # Check if server returns 400
    assert response.status_code == 400

    # Check if each dict contains these keys
    assert all(
        key in resp
        for key in ['error_code', 'message']
    ) is True


def test_post_unauthorized(client):
    headers = create_headers()

    category_id = 1
    data = {
        'name': 'My Item ({})'.format(random_string(10))
    }

    # Create item
    response = client.post(
        '/categories/{}/items'.format(category_id),
        headers=headers,
        data=json.dumps(data)
    )

    resp = json_response(response)

    # Check if server returns 401
    assert response.status_code == 401

    # Check if each dict contains these keys
    assert all(
        key in resp
        for key in ['message', 'error_code']
    ) is True
