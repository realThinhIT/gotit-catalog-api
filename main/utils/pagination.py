import math
from main.errors import ExceededRangePaginationError
from main.schemas.pagination import ResponsePaginationSchema


class PaginationUtils(object):
    @staticmethod
    def calc_pagination(page=1, per_page=50):
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
        pagination={},
        total=0
    ):
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
            items={}
        ):
            """
            Update payload that returns to the user with pagination information

            :param items: A list of items
            :return: Reponse payload
            """
            payload = {
                'items': items
            }

            payload.update(pagination.get('payload'))
            payload.update(pages)

            return ResponsePaginationSchema().load(payload)

        return create
