import json

from flask import Blueprint, request, Response, g
from db.google_db import DataAccess
from portfolio_api.utils.errors import Halt
from portfolio_api.utils.utilities import make_self_link, make_res
from portfolio_api.utils.closures import paginate

bp = Blueprint('boats', __name__, url_prefix='/boats')


@bp.route('', methods=["GET", "POST"])
@paginate('boat', 'boats', DataAccess)
def add_get_boat():
    res = Response()
    if request.method == 'POST':
        data = request.json
        try:
            boat_add = {
                "name": data["name"],
                "type": data["type"],
                "length": data["length"],
                "user": None,
                "loads": []
            }
            boat = DataAccess(kind='boat', namespace='boats')

        except KeyError:
            raise Halt('missing required property', 400)
        # ensure boat does not already exist
        if len(list(boat.get_all_filtered(('name', '=', boat_add["name"])))) \
                > 0:
            raise Halt('boat name already exists', 403)
        # add the boat
        boat.add_entity(boat_add)
        boat.entity["id"] = boat.entity.id
        make_self_link(boat.entity, request.base_url)
        res = make_res(boat.entity, 201)
    if request.method == 'GET':
        data = g.data["data"]
        next_link = g.data["next_link"]
        count = g.data["total_count"]
        # create self links
        for boat in data:
            for load in boat["loads"]:
                make_self_link(load, request.base_url, segment=1, kind='loads')
        for boat in data:
            make_self_link(boat, request.base_url)
            if boat["user"]:
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
def get_mod_boat(bid):
    # modifying a boat that belongs to a user required jwt
    pass


@bp.route('/<bid>/loads/<lid>', methods=["PUT", "DELETE"])
def add_remove_load(bid, lid):
    res = None
    boat = DataAccess(kind='boat', namespace='boats', eid=bid)
    load = DataAccess(kind='load', namespace='loads', eid=lid)
    if request.method == 'PUT':
        try:
            # ensure both boat and load exist
            boat.get_single_entity()
            load.get_single_entity()
            load.entity["id"] = load.entity.id
            boat.entity["id"] = boat.entity.id
        except ValueError:
            raise Halt('boat or load does not exist', 404)

        # ensure load isn't on another boat
        if load.entity["boat"] is not None:
            raise Halt('load is already on another boat', 400)
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
        res = '', 204
    return res

