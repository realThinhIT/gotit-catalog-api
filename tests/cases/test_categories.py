from tests.helpers import create_headers, json_response


def test_get_categories(client):
    response = client.get(
        '/categories',
        headers=create_headers()
    )

    resp = json_response(response)

    # Check if server returns 200
    assert response.status_code == 200

    # Check if number of categories equals to 4
    assert len(resp) == 4

    # Check if each dict contains these keys
    for res in resp:
        assert all(
            key in res
            for key in ['id', 'name', 'description', 'updated', 'created']
        ) is True


def test_get_valid_category(client):
    for category_id in range(1, 4):
        response = client.get(
            '/categories/{}'.format(category_id),
            headers=create_headers()
        )

        # Check if server returns 200
        assert response.status_code == 200

        # Check if these keys exists in response
        assert all(
            key in json_response(response).keys()
            for key in ['id', 'name', 'description', 'updated', 'created']
        ) is True


def test_get_invalid_category(client):
    for category_id in range(5, 7):
        response = client.get(
            '/categories/{}'.format(category_id),
            headers=create_headers()
        )

        # Check if server returns 404
        assert response.status_code == 404

        # Check if these keys exists in response
        assert all(
            key in json_response(response).keys()
            for key in ['message', 'error_code']
        ) is True
