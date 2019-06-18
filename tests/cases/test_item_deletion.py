from ..creation import _create_user, _create_item_in_category
from tests.helpers import create_headers, json_response, generate_access_token


def test_delete_item_authorized_valid_data(client):
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


def test_delete_item_authorized_deleted(client):
    # Init data
    category_id = 1

    user = _create_user(client)
    headers = create_headers(
        access_token=generate_access_token(user['id'])
    )
    item = _create_item_in_category(client, headers, category_id)
    item_id = item['id']

    # Delete item
    response = client.delete(
        '/categories/{}/items/{}'.format(category_id, item_id),
        headers=headers
    )

    # Check if server returns 200
    assert response.status_code == 200

    # Delete again
    response = client.delete(
        '/categories/{}/items/{}'.format(category_id, item_id),
        headers=headers
    )

    # Check if server returns 404
    assert response.status_code == 404


def test_delete_item_unauthorized_not_owned_valid_data(client):
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

    # Delete item
    response = client.delete(
        '/categories/{}/items/{}'.format(category_id, item_id),
        headers=headers2
    )

    # Check if server returns 403
    assert response.status_code == 403


def test_delete_item_unauthorized_valid_data(client):
    # Init data
    category_id = 1

    user = _create_user(client)

    headers = create_headers(
        access_token=generate_access_token(user['id'])
    )
    headers2 = create_headers()

    item = _create_item_in_category(client, headers, category_id)
    item_id = item['id']

    # Delete item
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
