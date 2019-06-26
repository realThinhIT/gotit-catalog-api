import json

from tests.helpers import create_headers, json_response, random_string


def _create_user(client):
    rand_string = random_string(10)

    credential = {
        'username': 'test{}'.format(rand_string),
        'password': rand_string,
        'name': 'Thinh Nguyen',
        'email': 'thinhnd.test{}@gmail.com'.format(rand_string)
    }

    response = client.post(
        '/users',
        headers=create_headers(),
        data=json.dumps(credential)
    )

    return json_response(response)


def _create_item_in_category(client, headers, category_id=1):
    data = {
        'name': 'My Item ({})'.format(random_string(10))
    }

    # Create item
    response = client.post(
        '/categories/{}/items'.format(category_id),
        headers=headers,
        data=json.dumps(data)
    )

    return json_response(response)
