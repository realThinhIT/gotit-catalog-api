import functools

from main.models import CategoryModel
from main.errors import NotFoundError


# A decorator that checks if the requested category id does exist, and
# pass an Category instance into route handler.
def parse_category(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        category = None

        # Retrieve the category
        requested_category_id = kwargs.get('category_id', None)

        if requested_category_id:
            category = CategoryModel.find_by_id(requested_category_id)

        # Handle errors
        if category:
            # Pass category to function
            kwargs.pop('category_id')
            kwargs['category'] = category

            return func(*args, **kwargs)
        else:
            # In case the category does not exist
            raise NotFoundError()
    return decorator
