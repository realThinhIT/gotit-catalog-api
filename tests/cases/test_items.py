from tests.helpers import create_headers, json_response, generate_access_token


def test_get_all_valid_items_without_authentication(client):
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


def test_get_all_valid_items_with_authentication(client):
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


def test_get_all_valid_items_with_invalid_pagination_with_authentication(client):
    for category_id in range(1, 4):
        response = client.get(
            '/categories/{}/items?page=abc'.format(category_id),
            headers=create_headers(
                access_token=generate_access_token(1)
            )
        )

        resp = json_response(response)

        # Check if server returns 400
        assert response.status_code == 400


def test_get_all_valid_items_with_exceeded_pagination_with_authentication(client):
    for category_id in range(1, 4):
        response = client.get(
            '/categories/{}/items?page=10'.format(category_id),
            headers=create_headers(
                access_token=generate_access_token(1)
            )
        )

        resp = json_response(response)

        # Check if server returns 400
        assert response.status_code == 400


def test_get_all_items_by_invalid_category_id(client):
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


def test_get_item_by_valid_category_id_and_id_without_auth(client):
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


def test_get_item_by_valid_category_id_and_id_with_auth(client):
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


def test_get_item_by_invalid_category_id_and_valid_item_id(client):
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
