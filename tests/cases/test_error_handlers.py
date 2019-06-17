import json
from tests.helpers import create_headers


def test_not_found(client):
    response = client.post(
        '/not-found',
        headers=create_headers()
    )

    # Check if server returns 404
    assert response.status_code == 404


def test_method_not_allowed(client):
    response = client.get(
        '/authentication',
        headers=create_headers()
    )

    # Check if server returns 405
    assert response.status_code == 405
