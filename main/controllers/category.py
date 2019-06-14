from main import app
from main.models import CategoryModel
from main.errors import NotFoundError
from main.schemas.category import CategorySchema
from main.response import json_response


@app.route('/categories', methods=['GET'])
@json_response
def get_all_categories():
    """
    Get all categories from the database

    :return: A list of existing categories
    """

    return CategorySchema(many=True).dump(CategoryModel.get_all())


@app.route('/categories/<int:category_id>', methods=['GET'])
@json_response
def get_category_by_id(category_id):
    """
    Get category information from the database using the given Category ID.

    :param category_id: ID of the category
    :return: Category object, otherwise
    """

    category = CategoryModel.find_by_id(category_id)

    if category is not None:
        return CategorySchema().dump(category)
    else:
        raise NotFoundError()
