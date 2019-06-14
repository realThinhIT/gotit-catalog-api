import functools
from main.models import CategoryModel
from main.errors import CategoryNotFoundError, NotFoundError


def valid_category_required(is_child=False, category_id_key='category_id'):
    def decorator_wrapper(func):
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            # Retrieve the category
            requested_category_id = kwargs.get(category_id_key, None)

            if requested_category_id:
                category = CategoryModel.find_by_id(requested_category_id)

            # Handle errors
            if category:
                # Pass category to function
                kwargs.pop(category_id_key)
                kwargs['category'] = category

                return func(*args, **kwargs)
            else:
                # If the resource is a child to category, raise category not found.
                # Otherwise, just raise not found.
                if is_child:
                    raise CategoryNotFoundError()
                else:
                    raise NotFoundError()
        return decorator
    return decorator_wrapper
