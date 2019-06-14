from flask_jwt import jwt_required, current_identity
from main import app
from main.response import json_response
from main.request import parse_with_pagination, validate_with_schema
from main.utils.category_validator import valid_category_required
from main.utils.pagination import PaginationUtils
from main.models.item import ItemModel
from main.schemas.item import ItemSchema, ItemSchemaRequest
from main.errors import NotFoundError, DuplicatedResourceError, InternalServerError, ForbiddenError


@app.route('/categories/<int:category_id>/items', methods=['GET'])
@parse_with_pagination
@valid_category_required(is_child=True)
@json_response
def get_items_in_category(category, pagination):
    """
    Get a list of items belong to a category.

    :param category:
    :param pagination:
    :return:
    """

    # Calculate total items
    total = ItemModel.count_items_by_category_id(category.id)
    payload_with_pagination = PaginationUtils.prepare_payload(
        pagination=pagination,
        total=total
    )

    # Retrieve a list of items
    items = ItemModel.get_all_with_pagination(
        offset=pagination.get('offset'),
        limit=pagination.get('limit')
    )

    # Returns a payload with pagination
    return payload_with_pagination(ItemSchema(many=True).load(items))


@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['GET'])
@valid_category_required(is_child=True)
@json_response
def get_item_in_category(item_id, category):
    item = category.items.filter_by(id=item_id).first()

    if item:
        return ItemSchema().dump(item)
    else:
        raise NotFoundError()


@app.route('/categories/<int:category_id>/items', methods=['POST'])
@jwt_required()
@valid_category_required(is_child=True)
@validate_with_schema(ItemSchemaRequest())
@json_response
def create_item_in_category(data, category):
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
        new_item.user_id = 1
        new_item.category_id = category.id

        new_item.save()
    except Exception:
        raise InternalServerError()

    return ItemSchema().dump(new_item)


@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['PUT'])
@jwt_required()
@valid_category_required(is_child=True)
@validate_with_schema(ItemSchemaRequest())
@json_response
def update_item_in_category(item_id, data, category):
    # Check if this item exists in the database
    item = category.items.filter_by(id=item_id).one_or_none()

    if item is None:
        raise NotFoundError()

    # Check if the user has the rights to modify this object
    if current_identity.id != item.user_id:
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

    return ItemSchema().dump(item)


@app.route('/categories/<int:category_id>/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
@valid_category_required(is_child=True)
@json_response
def delete_item_in_category(item_id, category):
    # Check if this item exists in the database
    item = category.items.filter_by(id=item_id).one_or_none()

    if item is None:
        raise NotFoundError()

    # Check if the user has the rights to modify this object
    if current_identity.id != item.user_id:
        raise ForbiddenError()

    # Proceed to update the item
    try:
        item.delete()
    except Exception:
        raise InternalServerError()

    return {
        'message': 'Item deleted successfully.'
    }, 200
