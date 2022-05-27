from db.google_db import DataAccess
from flask import Response
import json


def make_self_link(item, base, segment=0, kind=None):
    url = base.rsplit('/', segment)[0]
    if kind:
        url += '/' + kind
    if isinstance(item, list):
        for ob in item:
            ob["self"] = f'{url}/{ob["id"]}'
    else:
        entity_id = item.id if item.id else item["id"]
        item["self"] = f'{url}/{entity_id}'


def make_res(data, code, content_type='application/json'):
    res = Response()
    res.status_code = code
    res.content_type = content_type
    res.data = json.dumps(data)
    return res


def find_load_on_boat(boat, lid):
    for load in boat["loads"]:
        if str(load["id"]) == str(lid):
            return load


def update_loads_on_boat(loads: list):
    """
    prepares list of loads that need to be updated due to
    removal from boat
    """
    ready = []
    for index, load in enumerate(loads):
        load = DataAccess(kind="load", namespace="loads", eid=load["id"])
        ready.append(load)

    return ready


def make_next_link(base, token, limit):
    """ makes the next link string for pagination """
    return f"{base}?limit={limit}&page_token={token}"


