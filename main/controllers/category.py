from flask import jsonify
from main import app
from main.models import CategoryModel
from main.errors import NotFoundError
from main.schemas.category import CategorySchema


@app.route('/categories', methods=['GET'])
def get_all_categories():
    """
    Get all categories from the database

    :return: A list of existing categories
    """

    return jsonify(
        CategorySchema(many=True).dump(CategoryModel.get_all())
    ), 200


@app.route('/categories/<int:category_id>', methods=['GET'])
def get_category_info(category_id):
    """
    Get category information from the database using the given Category ID.

    :param category_id: ID of the category
    :return: Category object, otherwise
    """

    category = CategoryModel.find_by_id(category_id)

    if category is not None:
        return jsonify(
            CategorySchema().dump(category)
        ), 200
    else:
        raise NotFoundError()
