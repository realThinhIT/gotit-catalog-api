import math
from main.errors import ExceededRangePaginationError
from main.schemas.pagination import ResponsePaginationSchema


class PaginationUtils(object):
    @staticmethod
    def calc_pagination(page=1, per_page=50):
        """
        Calculate pagination information from payload.
        From page and per_page, calculate offset and limit for query statements.

        :param page: Current page
        :param per_page: Items per page
        :return: An object containing limit/ offset information
        """

        page = int(page)
        page = page if page > 0 else 1

        per_page = int(per_page)

        # Calculate pagination information
        offset = per_page * (page - 1)

        return {
            'page': page,
            'offset': offset,
            'limit': per_page,

            'payload': {
                'page': page,
                'per_page': per_page
            }
        }

    @staticmethod
    def calc_pages(total=0, per_page=50, page=None):
        """
        Calculate required pages from total items and items per page.

        :param total: Number of total items
        :param per_page: Items per page
        :param page: Current page
        :return: A payload contains pagination information
        """

        total = int(total)
        per_page = int(per_page)

        pages = int(math.ceil(total / float(per_page)))
        pages = pages if pages > 0 else 1

        return {
            'total': total,
            'page': page,
            'total_pages': pages,
            'has_next': page < pages
        }

    @staticmethod
    def prepare_payload(
        pagination=None,
        total=0
    ):
        """
        Prepare response with pagination.
        Be called to handle preparing payload, exceptions etc.

        :param pagination:
        :param total:
        :return: A function that can be called to create payload for the user
        """

        pages = PaginationUtils.calc_pages(
            total=total,
            per_page=pagination.get('limit'),
            page=pagination.get('page')
        )

        # If page requested larger than total pages
        if pagination.get('page') > pages.get('total_pages'):
            raise ExceededRangePaginationError({
                'page': [
                    'Max number of pages allowed: {}'.format(pages.get('total_pages'))
                ]
            })

        def create(
            items=None
        ):
            """
            Create a payload that returns to the user with pagination information.

            :param items: A list of items
            :return: Response payload
            """
            payload = {
                'items': items
            }

            payload.update(pagination.get('payload'))
            payload.update(pages)

            return ResponsePaginationSchema().load(payload)

        return create
