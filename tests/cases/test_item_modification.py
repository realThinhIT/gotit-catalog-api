import json
from ..creation import _create_user, _create_item_in_category
from tests.helpers import create_headers, json_response, generate_access_token, random_string


def test_put_authorized_valid_data(client):
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

    # Update item
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


def test_put_authorized_duplicated(client):
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

    # Update item
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


def test_put_authorized_invalid_data(client):
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

    # Update item
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


def test_put_authorized_unrecognized_field(client):
    # Init data
    category_id = 1

    user = _create_user(client)
    headers = create_headers(
        access_token=generate_access_token(user['id'])
    )
    item = _create_item_in_category(client, headers, category_id)
    item_id = item['id']

    data = {
        'id': 100,
        'name': 'New Item Name ({})'.format(random_string(100))
    }

    # Update item
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


def test_put_authorized_not_owned_valid_data(client):
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

    # Update item
    response = client.put(
        '/categories/{}/items/{}'.format(category_id, item_id),
        headers=headers2,
        data=json.dumps(data)
    )

    # Check if server returns 403
    assert response.status_code == 403


def test_put_unauthorized_valid_data(client):
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

    # Update item
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

