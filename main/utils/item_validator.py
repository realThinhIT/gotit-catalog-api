import functools
from main.errors import NotFoundError, ForbiddenError


def category_item_required(updating=False, item_id_key='item_id'):
    def item_required_wrapper(func):
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            category = kwargs['category']
            user = kwargs['user']
            item_id = kwargs[item_id_key]

            # Check if this item exists in the database
            item = category.items.filter_by(id=item_id).one_or_none()

            if item is None:
                raise NotFoundError()

            # Check if the user has the rights to modify this object
            if updating:
                if user.id != item.user_id:
                    raise ForbiddenError()

            # Pass item to the main function
            kwargs['item'] = item
            kwargs.pop(item_id_key)

            return func(*args, **kwargs)
        return decorator
    return item_required_wrapper
