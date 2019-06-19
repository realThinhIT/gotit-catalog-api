from tests.helpers import create_headers, json_response, generate_access_token


def test_get_unauthorized(client):
    for category_id in range(1, 4):
        response = client.get(
            '/categories/{}/items'.format(category_id),
            headers=create_headers()
        )

        resp = json_response(response)

        # Check if server returns 200
        assert response.status_code == 200

        # Check if pagination is correct
        assert all(
            key in resp
            for key in ['items', 'total_pages', 'page', 'total', 'per_page', 'has_next']
        ) is True

        # Check if each dict contains these keys
        for res in resp['items']:
            assert all(
                key in res
                for key in ['id', 'name', 'description', 'updated', 'created']
            ) is True

        # Check if is_owner not in item
        for res in resp['items']:
            assert 'is_owner' not in res


def test_get_invalid_authentication_type(client):
    for category_id in range(1, 4):
        response = client.get(
            '/categories/{}/items'.format(category_id),
            headers={
                'Authorization': 'JWT x'
            }
        )

        # Check if server returns 200
        assert response.status_code == 200


def test_get_invalid_jwt_authentication(client):
    for category_id in range(1, 4):
        response = client.get(
            '/categories/{}/items'.format(category_id),
            headers={
                'Authorization': 'Bearer XXXXX'
            }
        )

        # Check if server returns 200
        assert response.status_code == 200


def test_get_authorized(client):
    for category_id in range(1, 4):
        response = client.get(
            '/categories/{}/items'.format(category_id),
            headers=create_headers(
                access_token=generate_access_token(1)
            )
        )

        resp = json_response(response)

        # Check if server returns 200
        assert response.status_code == 200

        # Check if pagination is correct
        assert all(
            key in resp
            for key in ['items', 'total_pages', 'page', 'total', 'per_page', 'has_next']
        ) is True

        # Check if each dict contains these keys
        for res in resp['items']:
            assert all(
                key in res
                for key in [
                    'id', 'name', 'description', 'updated', 'created', 'is_owner'
                ]
            ) is True


def test_get_authorized_valid_pagination(client):
    response = client.get(
        '/categories/{}/items?page=1&per_page=1'.format(1),
        headers=create_headers(
            access_token=generate_access_token(1)
        )
    )

    resp = json_response(response)

    # Check if server returns 200
    assert response.status_code == 200

    # Check if pagination is correct
    assert all(
        key in resp
        for key in ['items', 'total_pages', 'page', 'total', 'per_page', 'has_next']
    ) is True

    # Check if it has 3 pages
    assert resp['total_pages'] == 3

    # Check if it has next page
    assert resp['has_next'] is True

    # Check if number of items is correct
    assert len(resp['items']) == 1


def test_get_authorized_valid_pagination_browse(client):
    for i in range(1, 2):
        response = client.get(
            '/categories/{}/items?page=1&per_page=2'.format(1, i),
            headers=create_headers(
                access_token=generate_access_token(1)
            )
        )

        resp = json_response(response)

        # Check if server returns 200
        assert response.status_code == 200

        # Check if pagination is correct
        assert all(
            key in resp
            for key in ['items', 'total_pages', 'page', 'total', 'per_page', 'has_next']
        ) is True

        # Check if it has 2 pages
        assert resp['total_pages'] == 2

        # Check if it has next page
        assert resp['has_next'] is (True if i == 1 else False)

        # Check if number of items is correct
        assert len(resp['items']) == (2 if i == 1 else 1)


def test_get_authorized_invalid_pagination(client):
    for category_id in range(1, 4):
        response = client.get(
            '/categories/{}/items?page=abc'.format(category_id),
            headers=create_headers(
                access_token=generate_access_token(1)
            )
        )

        # Check if server returns 400
        assert response.status_code == 400


def test_get_authorized_exceeded_pagination(client):
    for category_id in range(1, 4):
        response = client.get(
            '/categories/{}/items?page=10'.format(category_id),
            headers=create_headers(
                access_token=generate_access_token(1)
            )
        )

        # Check if server returns 400
        assert response.status_code == 400


def test_get_invalid_category_id(client):
    for category_id in range(5, 7):
        response = client.get(
            '/categories/{}/items'.format(category_id),
            headers=create_headers()
        )

        # Check if server returns 404
        assert response.status_code == 404

        # Check if these keys exists in response
        assert all(
            key in json_response(response).keys()
            for key in ['message', 'error_code']
        ) is True


def test_get_unauthorized_valid_category(client):
    category_id = 1

    for item_id in range(1, 3):
        response = client.get(
            '/categories/{}/items/{}'.format(category_id, item_id),
            headers=create_headers()
        )

        resp = json_response(response)

        # Check if server returns 200
        assert response.status_code == 200

        # Check if each dict contains these keys
        assert all(
            key in resp
            for key in ['id', 'name', 'description', 'updated', 'created']
        ) is True


def test_get_authorized_valid_category(client):
    category_id = 1

    for item_id in range(1, 3):
        response = client.get(
            '/categories/{}/items/{}'.format(category_id, item_id),
            headers=create_headers(
                access_token=generate_access_token(1)
            )
        )

        resp = json_response(response)

        # Check if server returns 200
        assert response.status_code == 200

        # Check if each dict contains these keys
        assert all(
            key in resp
            for key in ['id', 'name', 'description', 'updated', 'created', 'is_owner']
        ) is True


def test_get_invalid_category_valid_item(client):
    category_id = 3

    for item_id in range(1, 3):
        response = client.get(
            '/categories/{}/items/{}'.format(category_id, item_id),
            headers=create_headers()
        )

        # Check if server returns 404
        assert response.status_code == 404

        # Check if these keys exists in response
        assert all(
            key in json_response(response).keys()
            for key in ['message', 'error_code']
        ) is True


def test_get_valid_category_invalid_item(client):
    category_id = 1
    item_id = 10000

    response = client.get(
        '/categories/{}/items/{}'.format(category_id, item_id),
        headers=create_headers()
    )

    # Check if server returns 404
    assert response.status_code == 404

    # Check if these keys exists in response
    assert all(
        key in json_response(response).keys()
        for key in ['message', 'error_code']
    ) is True
