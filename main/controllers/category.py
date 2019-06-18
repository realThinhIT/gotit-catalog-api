from flask import jsonify
from main import app
from main.models import CategoryModel
from main.schemas.category import CategorySchema
from main.libs.resource_parsing.category import parse_category


@app.route('/categories', methods=['GET'])
def get_categories():
    """
    Get all categories from the database

    :return: A list of existing categories
    """

    return jsonify(
        CategorySchema(many=True).dump(CategoryModel.get_all())
    )


@app.route('/categories/<int:category_id>', methods=['GET'])
@parse_category(is_child_resource=False)
def get_category(category):
    """
    Get category information from the database using the given Category ID.

    :param category: The Category instance
    :return: Category object, otherwise
    """

    return jsonify(
        CategorySchema().dump(category)
    )
