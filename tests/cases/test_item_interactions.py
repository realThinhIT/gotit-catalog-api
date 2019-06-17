import json
import itertools
from ..creation import _create_user, _create_item_in_category
from tests.helpers import create_headers, json_response, generate_access_token, random_string


def test_create_new_item_with_auth(client):
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


def test_create_new_item_with_duplicated_content(client):
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


def test_create_new_item_with_invalid_input_with_auth(client):
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


def test_create_new_item_without_auth(client):
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


##########

def test_update_item_with_valid_data_with_auth(client):
    # Init data
    category_id = 1

    user = _create_user(client)
    headers = create_headers(
        access_token=generate_access_token(user['id'])
    )
    item = _create_item_in_category(client, headers, category_id)
    item_id = item['id']

    data = {
        'name': 'New Item Name ({})'.format(random_string(10))
    }

    # Create item
    response = client.put(
        '/categories/{}/items/{}'.format(category_id, item_id),
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

    # Check if new name matches
    assert resp['name'] == data['name']


def test_update_item_with_duplicated_data_with_auth(client):
    # Init data
    category_id = 1

    user = _create_user(client)
    headers = create_headers(
        access_token=generate_access_token(user['id'])
    )
    item = _create_item_in_category(client, headers, category_id)
    item2 = _create_item_in_category(client, headers, category_id)

    item_id = item['id']

    data = {
        'name': item2['name']
    }

    # Create item
    response = client.put(
        '/categories/{}/items/{}'.format(category_id, item_id),
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


def test_update_item_with_invalid_data_with_auth(client):
    # Init data
    category_id = 1

    user = _create_user(client)
    headers = create_headers(
        access_token=generate_access_token(user['id'])
    )
    item = _create_item_in_category(client, headers, category_id)
    item_id = item['id']

    data = {
        'name': 'New Item Name ({})'.format(random_string(100))
    }

    # Create item
    response = client.put(
        '/categories/{}/items/{}'.format(category_id, item_id),
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


def test_update_item_with_valid_data_with_invalid_auth(client):
    # Init data
    category_id = 1

    user = _create_user(client)
    user2 = _create_user(client)

    headers = create_headers(
        access_token=generate_access_token(user['id'])
    )
    headers2 = create_headers(
        access_token=generate_access_token(user2['id'])
    )

    item = _create_item_in_category(client, headers, category_id)
    item_id = item['id']

    data = {
        'name': 'New Item Name ({})'.format(random_string(10))
    }

    # Create item
    response = client.put(
        '/categories/{}/items/{}'.format(category_id, item_id),
        headers=headers2,
        data=json.dumps(data)
    )

    # Check if server returns 403
    assert response.status_code == 403


def test_update_item_with_valid_data_without_auth(client):
    # Init data
    category_id = 1

    user = _create_user(client)

    headers = create_headers(
        access_token=generate_access_token(user['id'])
    )
    headers2 = create_headers()

    item = _create_item_in_category(client, headers, category_id)
    item_id = item['id']

    data = {
        'name': 'New Item Name ({})'.format(random_string(10))
    }

    # Create item
    response = client.put(
        '/categories/{}/items/{}'.format(category_id, item_id),
        headers=headers2,
        data=json.dumps(data)
    )

    resp = json_response(response)

    # Check if server returns 401
    assert response.status_code == 401

    # Check if each dict contains these keys
    assert all(
        key in resp
        for key in ['error_code', 'message']
    ) is True


#######

def test_delete_item_with_valid_data_with_auth(client):
    # Init data
    category_id = 1

    user = _create_user(client)
    headers = create_headers(
        access_token=generate_access_token(user['id'])
    )
    item = _create_item_in_category(client, headers, category_id)
    item_id = item['id']

    # Create item
    response = client.delete(
        '/categories/{}/items/{}'.format(category_id, item_id),
        headers=headers
    )

    resp = json_response(response)

    # Check if server returns 200
    assert response.status_code == 200

    # Check if each dict contains these keys
    assert all(
        key in resp
        for key in ['message']
    ) is True


def test_delete_item_with_valid_data_with_invalid_auth(client):
    # Init data
    category_id = 1

    user = _create_user(client)
    user2 = _create_user(client)

    headers = create_headers(
        access_token=generate_access_token(user['id'])
    )
    headers2 = create_headers(
        access_token=generate_access_token(user2['id'])
    )

    item = _create_item_in_category(client, headers, category_id)
    item_id = item['id']

    # Create item
    response = client.delete(
        '/categories/{}/items/{}'.format(category_id, item_id),
        headers=headers2
    )

    # Check if server returns 403
    assert response.status_code == 403


def test_delete_item_with_valid_data_without_auth(client):
    # Init data
    category_id = 1

    user = _create_user(client)

    headers = create_headers(
        access_token=generate_access_token(user['id'])
    )
    headers2 = create_headers()

    item = _create_item_in_category(client, headers, category_id)
    item_id = item['id']

    # Create item
    response = client.put(
        '/categories/{}/items/{}'.format(category_id, item_id),
        headers=headers2
    )

    resp = json_response(response)

    # Check if server returns 401
    assert response.status_code == 401

    # Check if each dict contains these keys
    assert all(
        key in resp
        for key in ['error_code', 'message']
    ) is True
