import json

from flask import Blueprint, request, Response, g
from db.google_db import DataAccess
from portfolio_api.utils.errors import Halt
from portfolio_api.utils.utilities import make_self_link, make_res, \
    find_load_on_boat, update_loads_on_boat
from portfolio_api.utils.paginate import paginate
from portfolio_api.auth.validate import validating

bp = Blueprint('boats', __name__, url_prefix='/boats')


@bp.route('', methods=["GET", "POST"])
@validating(errors=True)
def add_get_boat():
    res = Response()
    sub = g.jwt_payload["sub"]
    boat = DataAccess(kind='boat', namespace='boats')
    user = DataAccess(kind='user', namespace='users')
    if request.method == 'POST':

        data = request.json
        try:
            boat_add = {
                "name": data["name"],
                "type": data["type"],
                "length": data["length"],
                "user": sub,
                "loads": []
            }
        except KeyError:
            raise Halt('missing required property', 400)
        # ensure boat does not already exist
        if len(
                list(boat.get_all_filtered(
                    [('name', '=', boat_add["name"])]
                    )
                )
        ) > 0:
            raise Halt('a boat with this name already exists', 403)
        # add the boat
        boat.add_entity(boat_add)
        boat.entity["id"] = boat.entity.id
        # get user in db and update boats property
        user.entity = list(user.get_all_filtered([('sub', '=', sub)])).pop()
        boat_data = boat.entity.copy()
        # only add data on boats to user
        boat_data.pop('loads')
        user.entity["boats"].append(boat_data)
        user.update_only_single()

        make_self_link(boat.entity, request.base_url)
        res = make_res(boat.entity, 201)
    if request.method == 'GET':
        data, next_link, count = paginate(
            boat,
            use_filter=[('user', '=', sub)]
        )
        # create self links
        for boat in data:
            for load in boat["loads"]:
                make_self_link(load, request.base_url, segment=1, kind='loads')
        for boat in data:
            make_self_link(boat, request.base_url)
            make_self_link(boat["user"], request.base_url, segment=1,
                           kind='users')
        res_data = {
            "self": request.url,
            "boats": data,
            "next": next_link,
            "total_count": count
        }
        res = make_res(res_data, 200)
    return res


@bp.route('/<bid>', methods=["GET", "PUT", "PATCH", "DELETE"])
@validating(errors=True)
def get_mod_boat(bid):
    # modifying a boat that belongs to a user required jwt
    boat = DataAccess(kind='boat', namespace='boats', eid=bid)
    user_id = g.jwt_payload["sub"]
    try:
        # ensure boat exists
        boat.get_single_entity()
        boat.entity["id"] = boat.entity.id
    except ValueError:
        raise Halt('boat or load does not exist', 404)
    # ensure valid jwt and boat belongs to user with jwt
    if boat.entity["user"] != user_id:
        raise Halt('user is not authorized to access this boat', 401)

    if request.method == 'GET':
        make_self_link(
            boat.entity["loads"],
            request.base_url,
            segment=2,
            kind='loads'
        )
        boat.entity["self"] = request.url
        return make_res(boat.entity, 200)
    if request.method == 'DELETE':
        boat.delete_entity(get=False)
        update_loads_boat(boat)
        update_user_boats(user_id, boat)
        return '', 204

    if request.method == 'PUT':
        data = request.json
        boat_name = data.get('name')
        name_exists(boat_name, boat.entity["name"])
        boat.update_only_single(data)
    if request.method == 'PATCH':
        data = request.json
        boat_name = data.get("name")
        name_exists(boat_name, boat.entity["name"])
        boat.update_only_single(data)

    update_loads_boat(boat)
    update_user_boats(user_id, boat)
    boat.entity["self"] = request.url
    make_self_link(boat.entity["loads"], request.base_url, segment=2,
                   kind='loads')
    return make_res(boat.entity, 200)


def name_exists(boat_name, cur_name):
    # if name to be changed
    if boat_name != cur_name:
        is_boat = DataAccess(kind='boat', namespace='boats')
        result = list(is_boat.get_all_filtered([('name', '=', boat_name)]))
        if len(result) > 0:
            raise Halt('a boat with this name already exists', 403)


def update_loads_boat(boat):

    load_boat_ob = boat.entity.copy()
    load_boat_ob.pop('loads')
    all_loads = update_loads_on_boat(boat.entity["loads"])

    if request.method == 'PUT' or request.method == 'PATCH':
        with boat.get_db_instance().transaction():
            for load in all_loads:
                load.get_single_entity()
                load.entity["boat"] = load_boat_ob
                load.update_only_single()

    if request.method == "DELETE":
        with boat.get_db_instance().transaction():
            for load in all_loads:
                load.get_single_entity()
                load.entity["boat"] = None
                load.update_only_single()


def update_user_boats(user_id, boat):
    boat_entity = boat.entity.copy()
    user = DataAccess(kind='user', namespace='users')
    user.entity = list(user.get_all_filtered([('sub', '=', user_id)])).pop()
    for index, cur in enumerate(user.entity["boats"]):
        if cur["id"] == boat.entity.id:
            if request.method == 'DELETE':
                user.entity["boats"].remove(cur)
            if request.method == 'PUT' or request.method == 'PATCH':
                boat_entity.pop('loads')
                user.entity["boats"][index] = boat_entity
            return user.update_only_single()


@bp.route('/<bid>/loads/<lid>', methods=["PUT", "DELETE"])
@validating(errors=True)
def add_remove_load(bid, lid):
    boat = DataAccess(kind='boat', namespace='boats', eid=bid)
    load = DataAccess(kind='load', namespace='loads', eid=lid)
    try:
        # ensure both boat and load exist
        boat.get_single_entity()
        load.get_single_entity()
        load.entity["id"] = load.entity.id
        boat.entity["id"] = boat.entity.id
    except ValueError:
        raise Halt('boat or load does not exist', 404)

    if request.method == 'PUT':

        # ensure load isn't on another boat
        if load.entity["boat"] is not None:
            raise Halt('this load is on another boat', 400)
        all_loads = boat.entity["loads"]
        all_loads.append({
            "id": load.entity.id,
            "type": load.entity["type"],
            "weight": load.entity["weight"],
            "length": load.entity["length"],
        })

        boat.update_only_single({"loads": all_loads})
        load.update_only_single({"boat": {
            "id": boat.entity["id"],
            "name": boat.entity["name"],
            "type": boat.entity["type"],
            "length": boat.entity["length"]
        }})

    if request.method == 'DELETE':
        # ensure the load is on this boat
        boat_id = load.entity["boat"].get('id')
        # load not on this boat
        if str(boat_id) != str(bid):
            raise Halt('this load is not on this boat', 400)
        load_on = find_load_on_boat(boat.entity, lid)
        boat.entity["loads"].remove(load_on)
        load.entity["boat"] = None
        boat.update_only_single()
        load.update_only_single()
        return '', 204

    make_self_link(
        boat.entity["loads"],
        request.base_url,
        segment=4,
        kind='loads'
    )
    boat.entity["self"] = request.url
    return make_res(boat.entity, 200)


