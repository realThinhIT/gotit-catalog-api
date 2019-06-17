from flask import jsonify
from main import app
from main.request import parse_with_pagination, validate_with_schema
from main.utils.category_validator import valid_category_required
from main.utils.pagination import PaginationUtils
from main.models.item import ItemModel
from main.schemas.item import ItemSchema, ItemSchemaRequest
from main.errors import NotFoundError, DuplicatedResourceError, InternalServerError, ForbiddenError
from main.security import requires_authentication, optional_authentication


# TODO: Make a new is_owner field for authenticated users
@app.route('/categories/<int:category_id>/items', methods=['GET'])
@parse_with_pagination
@optional_authentication
@valid_category_required(is_child=True)
def get_all_items(category, user, pagination):
    """
    Get a list of items belong to a category.

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


# TODO: Make a new is_owner field for authenticated users
@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['GET'])
@optional_authentication
@valid_category_required(is_child=True)
def get_item(item_id, user, category):
    """
    Get a specific item from a category given an ID.

    :param item_id: ID of the item
    :param user: User instance of the authenticated user
    :param category: Category from which the item is being retrieved
    :return: Item information
    """

    item = category.items.filter_by(id=item_id).first()

    if item:
        # If authentication is provided,
        # update is_owner
        if user:
            item.is_owner = item.user_id == user.id

        return jsonify(
            ItemSchema().dump(item)
        ), 200
    else:
        raise NotFoundError()


@app.route('/categories/<int:category_id>/items', methods=['POST'])
@requires_authentication
@valid_category_required(is_child=True)
@validate_with_schema(ItemSchemaRequest())
def create_item(data, user, category):
    """
    Create a new item in the given category.

    :param data: The data of the item
    :param user: User instance of the authenticated user
    :param category: Category from which the item is being created
    :return: A newly created Item
    """

    # Check if the category already has an item with the same name
    duplicated_item = category.items.filter_by(name=data.get('name')).one_or_none()

    if duplicated_item:
        raise DuplicatedResourceError({
            'name': 'An item with name "{}" already exist in this category. '
                    'Please try another name.'.format(data.get('name'))
        })

    # Proceed to create new item in category
    try:
        new_item = ItemModel(**data)
        new_item.user_id = user.id
        new_item.category_id = category.id

        new_item.save()
    except Exception:
        raise InternalServerError()

    return jsonify(
        ItemSchema().dump(new_item)
    ), 200


@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['PUT'])
@requires_authentication
@valid_category_required(is_child=True)
@validate_with_schema(ItemSchemaRequest())
def update_item(item_id, data, user, category):
    """
    Update an existing item with new data.
    Note that only the one who owns the resource can update it.

    :param item_id: ID of the item
    :param data: The new data of the item
    :param user: User instance of the authenticated user
    :param category: Category from which the item is being retrieved
    :return:
    """

    # Check if this item exists in the database
    item = category.items.filter_by(id=item_id).one_or_none()

    if item is None:
        raise NotFoundError()

    # Check if the user has the rights to modify this object
    if user.id != item.user_id:
        raise ForbiddenError()

    # Check if the category already has an item with the same name
    duplicated_item = category.items.filter_by(name=data.get('name')).one_or_none()

    if duplicated_item:
        raise DuplicatedResourceError({
            'name': 'An item with name "{}" already exist in this category. '
                    'Please try another name.'.format(data.get('name'))
        })

    # Proceed to update the item
    try:
        item.update(**data)
        item.save()
    except Exception:
        raise InternalServerError()

    return jsonify(
        ItemSchema().dump(item)
    ), 200


@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['DELETE'])
@requires_authentication
@valid_category_required(is_child=True)
def delete_item(item_id, user, category):
    """
    Delete an existing item in the database.
    Note that only the one who owns the resource can delete it.

    :param item_id: ID of the item
    :param user: User instance of the authenticated user
    :param category: Category from which the item is being retrieved
    :return:
    """

    # Check if this item exists in the database
    item = category.items.filter_by(id=item_id).one_or_none()

    if item is None:
        raise NotFoundError()

    # Check if the user has the rights to modify this object
    if user.id != item.user_id:
        raise ForbiddenError()

    # Proceed to update the item
    try:
        item.delete()
    except Exception, e:
        print(e)
        raise InternalServerError()

    return jsonify({
        'message': 'Item deleted successfully.'
    }), 200
