import functools

from main.errors import NotFoundError, ForbiddenError


# A decorator that checks for valid item from item_id_key, and pass it to route handler
# for future processing.
# Requires having category and user in kwargs, or using these decorators in advance:
# - @optional_authentication / @requires_authentication
# - @parse_category
def parse_category_item(requires_ownership=False):
    def item_required_wrapper(func):
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            category = kwargs['category']
            user = kwargs['user']
            item_id = kwargs['item_id']

            # Check if this item exists in the database
            item = category.items.filter_by(id=item_id).one_or_none()

            if item is None:
                raise NotFoundError()

            # Check if the user has the rights to modify this object
            if requires_ownership:
                if user.id != item.user_id:
                    raise ForbiddenError()

            # Pass item to the main function
            kwargs['item'] = item
            kwargs.pop('item_id')

            return func(*args, **kwargs)
        return decorator
    return item_required_wrapper
