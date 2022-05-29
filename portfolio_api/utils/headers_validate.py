from flask import request
from functools import wraps
from portfolio_api.utils.errors import Halt


def accept_validate_parent(mime_type='application/json'):
    def accept_validate(func):
        @wraps(func)
        def validator(*args, **kwargs):
            if request.headers.get('Accept') not in [mime_type, '*/*']\
                    and request.method != 'DELETE':
                raise Halt(f'accept mime type must be {mime_type}', 406)
            return func(*args, **kwargs)

        return validator

    return accept_validate


