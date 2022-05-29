from flask import Response, request
import json


class Halt(Exception):

    def __init__(self, err: str, code: int):
        self.err = {"error": err}
        self.code = code


def any_error(err):
    res = Response()
    res.status_code = err.code
    res.data = json.dumps(err.err)
    res.content_type = 'application/json'
    return res


def method_error(err):
    res = Response()
    res.status_code = err.code
    res.data = json.dumps({"error": f"{request.method} method not allowed for "
                                    f"this url"})
    res.content_type = 'application/json'
    return res

