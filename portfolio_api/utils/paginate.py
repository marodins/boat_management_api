from flask import request
from portfolio_api.utils.utilities import make_next_link


def paginate(entry, use_filter: list = None):
    link = None
    limit = int(request.args.get('limit', 5))
    page_token = request.args.get('page_token', None)
    with entry.get_db_instance().transaction():
        if use_filter:
            quantity = len(list(entry.get_all_filtered(use_filter)))
            results = entry.get_all_paginated(
                limit=limit,
                start_cursor=page_token,
                all_filters=use_filter
            )
        else:
            quantity = len(entry.get_all())
            results = entry.get_all_paginated(
                limit=limit,
                start_cursor=page_token
            )
    pages = next(results.pages)
    loaded = list(pages)

    if results.next_page_token:
        token = results.next_page_token.decode()
        link = make_next_link(request.base_url, token, limit)

    return loaded, link, quantity
