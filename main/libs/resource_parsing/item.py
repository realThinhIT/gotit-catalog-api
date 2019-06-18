import functools
from main.errors import NotFoundError, ForbiddenError, DuplicatedResourceError


# A decorator that checks for valid item from item_id_key, and pass it to route handler
# for future processing.
def parse_category_item(requires_ownership=False, item_id_key='item_id'):
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
            if requires_ownership:
                if user.id != item.user_id:
                    raise ForbiddenError()

            # Pass item to the main function
            kwargs['item'] = item
            kwargs.pop(item_id_key)

            return func(*args, **kwargs)
        return decorator
    return item_required_wrapper


# A decorator that checks for duplicated name in the same category
# while updating, or creating new item.
def requires_item_unique_name(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        data = kwargs['data']
        category = kwargs['category']

        # Check if the category already has an item with the same name
        duplicated_item = category.items.filter_by(name=data.get('name')).one_or_none()

        # Check if different items
        try:
            item = kwargs['item'] or None

            if duplicated_item:
                different_item = item.id != duplicated_item.id
            else:
                different_item = True
        except KeyError:
            different_item = True

        # In case they are not the same item
        if duplicated_item and different_item:
            raise DuplicatedResourceError({
                'name': [
                    'An item with name "{}" already exists in this category. '
                    'Please try another name.'.format(data.get('name'))
                ]
            })

        return func(*args, **kwargs)
    return decorator
