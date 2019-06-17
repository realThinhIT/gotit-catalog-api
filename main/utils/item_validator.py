import functools
from main.errors import NotFoundError, ForbiddenError, DuplicatedResourceError


def category_item_required(needs_ownership=False, item_id_key='item_id'):
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
            if needs_ownership:
                if user.id != item.user_id:
                    raise ForbiddenError()

            # Pass item to the main function
            kwargs['item'] = item
            kwargs.pop(item_id_key)

            return func(*args, **kwargs)
        return decorator
    return item_required_wrapper


def category_item_unique_name_required(func):
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
