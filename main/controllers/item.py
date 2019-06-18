from flask import jsonify
from main import app
from main.models.item import ItemModel
from main.schemas.item import ItemSchema, ItemSchemaRequest
from main.libs.resource_parsing.common import parse_with_pagination, parse_with_schema
from main.libs.resource_parsing.category import parse_category
from main.libs.pagination import PaginationUtils
from main.libs.authentication import require_authentication, optional_authentication
from main.libs.resource_parsing.item import parse_category_item, requires_item_unique_name


# noinspection PyUnresolvedReferences
@app.route('/categories/<int:category_id>/items', methods=['GET'])
@parse_with_pagination
@optional_authentication
@parse_category(is_child_resource=True)
def get_items(category, user, pagination):
    """Get a list of items belong to a category.

    category_id is not needed as it was resolved by a decorator as category
    :param category: Category from which the item is being retrieved
    :param user: User instance of the authenticated user
    :param pagination: Pagination information
    :return: A list of items with pagination information
    """

    # Calculate total items
    total = ItemModel.count_items_by_category_id(category.id)
    payload_with_pagination = PaginationUtils.prepare_payload(
        pagination=pagination,
        total=total
    )

    # Retrieve a list of items
    items = ItemModel.get_with_pagination_by_category_id(
        category_id=category.id,
        offset=pagination.get('offset'),
        limit=pagination.get('limit')
    )

    # If authentication is provided,
    # update is_owner
    if user:
        for item in items:
            item.is_owner = item.user_id == user.id

    # Returns a payload with pagination
    return jsonify(
        payload_with_pagination(
            ItemSchema(many=True).dump(items)
        )
    )


# noinspection PyUnresolvedReferences
@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['GET'])
@optional_authentication
@parse_category(is_child_resource=True)
@parse_category_item(requires_ownership=False)
def get_item(item, user, **_):
    """Get a specific item from a category given an ID.

    category_id is not needed as it was resolved by a decorator as category
    item_id is not needed as it was resolved by a decorator as item
    :param item: Item instance
    :param user: User instance of the authenticated user
    :return: Item information
    """

    # If authentication is provided,
    # update is_owner
    if user:
        item.is_owner = item.user_id == user.id

    return jsonify(
        ItemSchema().dump(item)
    )


# noinspection PyUnresolvedReferences
@app.route('/categories/<int:category_id>/items', methods=['POST'])
@require_authentication
@parse_category(is_child_resource=True)
@parse_with_schema(ItemSchemaRequest())
@requires_item_unique_name
def create_item(data, user, category):
    """Create a new item in the given category.

    category_id is not needed as it was resolved by a decorator as category
    :param data: The data of the item
    :param user: User instance of the authenticated user
    :param category: Category from which the item is being created
    :return: A newly created Item
    """

    # Proceed to create new item in category
    new_item = ItemModel(**data)
    new_item.user_id = user.id
    new_item.category_id = category.id

    new_item.save()

    return jsonify(
        ItemSchema().dump(new_item)
    )


# noinspection PyUnresolvedReferences
@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['PUT'])
@require_authentication
@parse_category(is_child_resource=True)
@parse_category_item(requires_ownership=True)
@parse_with_schema(ItemSchemaRequest())
@requires_item_unique_name
def update_item(item, data, **_):
    """Update an existing item with new data.
    Note that only the one who owns the resource can update it.

    category_id is not needed as it was resolved by a decorator as category
    item_id is not needed as it was resolved by a decorator as item
    :param item: Item instance
    :param data: The new data of the item
    :return:
    """

    # Proceed to update the item
    item.update(**data)
    item.save()

    return jsonify(
        ItemSchema().dump(item)
    )


# noinspection PyUnresolvedReferences
@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['DELETE'])
@require_authentication
@parse_category(is_child_resource=True)
@parse_category_item(requires_ownership=True)
def delete_item(item, **_):
    """Delete an existing item in the database.
    Note that only the one who owns the resource can delete it.

    category_id is not needed as it was resolved by a decorator as category
    category_id is not needed as it was resolved by a decorator as item_id
    :param item: Item instance
    :return:
    """

    # Proceed to update the item
    item.delete()

    return jsonify({
        'message': 'Item deleted successfully.'
    })

