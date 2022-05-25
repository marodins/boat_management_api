from flask import request, g
from functools import wraps
from utilities import make_next_link


def paginate(data_kind, namespace, Access):
    def paginate_result(func):
        @wraps(func)
        def paginate_closure(*args, **kwargs):
            if request.method == 'GET':
                entry = Access(kind=data_kind, namespace=namespace)
                link = None
                limit = int(request.args.get('limit', 5))
                page_token = request.args.get('page_token', None)
                results = entry.get_all(limit=limit, start_cursor=page_token)
                pages = next(results.pages)
                loaded = list(pages)
                token = None
                if results.next_page_token:
                    token = results.next_page_token.decode()
                if token:
                    link = make_next_link(request.base_url, token, limit)
                g.data = {
                    "next_link": link,
                    "data": loaded,
                    "total_count": len(loaded)
                }
                return func(*args, **kwargs)
        return paginate_closure
    return paginate_result

