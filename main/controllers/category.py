from flask import jsonify
from main import app
from main.models import CategoryModel
from main.errors import NotFoundError
from main.schemas.category import CategorySchema
from main.utils.category_validator import valid_category_required


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
@valid_category_required(is_child=False)
def get_category_info(category):
    """
    Get category information from the database using the given Category ID.

    :param category: The Category instance
    :return: Category object, otherwise
    """

    return jsonify(
        CategorySchema().dump(category)
    ), 200
