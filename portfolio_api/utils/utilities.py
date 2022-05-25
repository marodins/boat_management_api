from db.google_db import DataAccess
from flask import Response
import json


def make_self_link(item, base, segment=0, kind=None):
    url = base.rsplit('/', segment)[0]
    entity_id = item.id if item.id else item["id"]
    if kind:
        url += '/' + kind
    item["self"] = f'{url}/{entity_id}'


def make_res(data, code, content_type='application/json'):
    res = Response()
    res.status_code = code
    res.content_type = content_type
    res.data = json.dumps(data)
    return res


def delete_load_on_boat(lid, boat, error=True):
    """
    deletes a load from a boat instance raises error if load was not found
    only if error is True
    :param lid: load id
    :param boat: boat instance of DataAccess type
    :param error: bool-if error needs to be raised when no load on boat found
    :return: None
    """
    for load in boat.entity["loads"]:
        if str(lid) == str(load["id"]):
            boat.entity["loads"].remove(load)
            return
    if error:
        raise ValueError


def delete_boat_from_load(loads: list):
    """
    prepares list of loads that need to be updated due to
    removal from boat
    """
    ready = []
    for index, load in enumerate(loads):
        load = DataAccess(kind="load", namespace="loads", eid=load["id"])
        ready.append(load)

    return ready


def find_item_in(all_objects, bid):
    find = None
    for item in all_objects:
        if item["id"] == bid:
            find = item

    return find


def make_next_link(base, token, limit):
    """ makes the next link string for pagination """
    return f"{base}?limit={limit}&page_token={token}"
