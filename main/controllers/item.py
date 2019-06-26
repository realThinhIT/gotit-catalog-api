from flask import jsonify, request
from marshmallow import ValidationError

from main import app
from main.errors import InvalidPaginationFormatError, ExceededRangePaginationError, DuplicatedItemError
from main.models.item import ItemModel
from main.schemas.item import ItemSchema
from main.schemas.pagination import RequestPaginationSchema, ResponsePaginationSchema
from main.libs.resource_parsing.common import parse_with_schema
from main.libs.resource_parsing.category import parse_category
from main.libs.authentication import require_authentication, optional_authentication
from main.libs.resource_parsing.item import parse_category_item


# noinspection PyUnresolvedReferences
@app.route('/categories/<int:category_id>/items', methods=['GET'])
@optional_authentication
@parse_category
def get_items(category, user):
    """Get a list of items belong to a category.

    category_id is not needed as it was resolved by a decorator as category
    :param category: Category from which the item is being retrieved
    :param user: User instance of the authenticated user
    :return: A list of items with pagination information
    """

    # Validate pagination information
    try:
        pagination = RequestPaginationSchema().load(request.args)
    except ValidationError:
        raise InvalidPaginationFormatError

    # Get items with pagination
    items = category.items \
                    .paginate(page=pagination.get('page'),
                              per_page=pagination.get('per_page'),
                              error_out=False)

    # In case the user get an out-of-range page
    if pagination.get('page') > items.pages:
        raise ExceededRangePaginationError()

    # If authentication is provided,
    # update is_owner
    if user:
        for item in items.items:
            item.is_owner = item.user_id == user.id

    # Returns a payload with pagination
    return jsonify(ResponsePaginationSchema().load({
        'items': ItemSchema(many=True).dump(items.items),
        'total': items.total,
        'total_pages': items.pages,
        'page': items.page,
        'per_page': items.per_page
    }))


# noinspection PyUnresolvedReferences
@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['GET'])
@optional_authentication
@parse_category
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
@parse_category
@parse_with_schema(ItemSchema())
def create_item(data, user, category):
    """Create a new item in the given category.

    category_id is not needed as it was resolved by a decorator as category
    :param data: The data of the item
    :param user: User instance of the authenticated user
    :param category: Category from which the item is being created
    :return: A newly created Item
    """

    # Check if the category already has an item with the same name
    duplicated_item = category.items.filter_by(name=data.get('name')).one_or_none()

    if duplicated_item:
        raise DuplicatedItemError()

    # Proceed to create new item in category
    new_item = ItemModel(**data)
    new_item.user_id = user.id
    new_item.category_id = category.id

    # Save to DB
    new_item.save()

    return jsonify(
        ItemSchema().dump(new_item)
    )


# noinspection PyUnresolvedReferences
@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['PUT'])
@require_authentication
@parse_category
@parse_category_item(requires_ownership=True)
@parse_with_schema(ItemSchema())
def update_item(item, data, category, **_):
    """Update an existing item with new data.
    Note that only the one who owns the resource can update it.

    category_id is not needed as it was resolved by a decorator as category
    item_id is not needed as it was resolved by a decorator as item
    :param item: Item instance
    :param data: The new data of the item
    :param category: The category of this item
    :return:
    """

    # Check if the category already has an item with the same name
    duplicated_item = category.items.filter_by(name=data.get('name')).one_or_none()

    if duplicated_item and duplicated_item.id != item.id:
        raise DuplicatedItemError()

    # Proceed to update the item
    item.update(**data)
    item.save()

    return jsonify(
        ItemSchema().dump(item)
    )


# noinspection PyUnresolvedReferences
@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['DELETE'])
@require_authentication
@parse_category
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

