from flask import Blueprint, request, g
from portfolio_api.utils.errors import Halt
from db.google_db import DataAccess
from portfolio_api.utils.utilities import make_res, make_self_link, find_load_on_boat
from portfolio_api.utils.paginate import paginate
from portfolio_api.utils.headers_validate import accept_validate_parent
from portfolio_api.auth.validate import validating

bp = Blueprint('loads', __name__, url_prefix='/loads')


@bp.route('', methods=["GET", "POST"])
@accept_validate_parent()
def add_get_loads():
    load = DataAccess(kind="load", namespace="loads")
    res = None
    if request.method == 'POST':
        data = request.json
        try:
            load_type = data["type"]
            weight = data["weight"]
            volume = data["volume"]

            load.add_entity({
                "type": load_type,
                "weight": weight,
                "volume": volume,
                "boat": None
            })
            load.entity["id"] = load.entity.id
            make_self_link(load.entity, request.base_url)
            res = make_res(load.entity, 201)
        except KeyError:
            raise Halt('missing required attribute', 400)

    if request.method == 'GET':
        data, next_link, count = paginate(load)
        # create self links
        for load in data:
            make_self_link(load, request.base_url)
            if load["boat"]:
                make_self_link(load["boat"], request.base_url, segment=1,
                               kind='boats')
        res_data = {
            "self": request.url,
            "loads": data,
            "next": next_link,
            "total_count": count
        }
        res = make_res(res_data, 200)

    return res


@bp.route('/<lid>', methods=["GET", "PUT", "PATCH", "DELETE"])
@accept_validate_parent()
@validating()
def specific_load(lid):
    load = DataAccess(kind='load', namespace='loads', eid=lid)
    res = None
    try:
        load.get_single_entity()
    except ValueError:
        raise Halt('this load does not exist', 404)

    if request.method == 'GET':
        res = get_load(load)
    else:
        # if load is on a boat require jwt for write operation
        if load.entity["boat"]:
            if not g.error:
                sub = g.jwt_payload["sub"]
                if load.entity["boat"]["id"] != sub:
                    raise Halt('this load is on a boat, invalid token for '
                               'boat owner', 401)
            # if error exists
            else:
                raise Halt('this load is on a boat, please provide valid auth '
                           'token', 401)
        if request.method == 'PUT' or request.method == 'PATCH':
            res = update_loads_boat(load, lid)
        if request.method == 'DELETE':
            res = delete_and_update(load, lid)

    return res


def get_load(load):
    load.entity["self"] = request.url
    if load.entity["boat"]:
        make_self_link(load.entity["boat"], request.base_url, segment=2,
                       kind='boats')
    return make_res(load.entity, 200)


def update_loads_boat(load, lid):
    data = request.json
    load.update_only_single(data)
    # this load is on a boat, update boat
    if load.entity["boat"]:
        boat = DataAccess(
            kind='boat',
            namespace='boats',
            eid=load.entity["boat"]["id"]
        )
        boat.get_single_entity()
        load_boat = find_load_on_boat(boat.entity, lid)
        # updated that specific load on the boat
        load_boat.update(data)
        boat.update_only_single()
        make_self_link(load.entity["boat"], request.base_url, segment=2,
                       kind='boats')
    load.entity["self"] = request.url
    return make_res(load.entity, 200)


def delete_and_update(load, lid):
    if load.entity["boat"]:
        boat = DataAccess(
            kind='boat',
            namespace='boats',
            eid=load.entity["boat"]["id"]
        )
        boat.get_single_entity()
        load_boat = find_load_on_boat(boat.entity, lid)
        boat.entity["loads"].remove(load_boat)
        boat.update_only_single()
    load.delete_entity()
    return '', 204

