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
                "owner": None,
                "load": None
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
        # create self links
        pass

    return res


@bp.route('/<bid>', methods=["GET", "PUT", "PATCH", "DELETE"])
def get_mod_boat(bid):
    # modifying a boat that belongs to a user required jwt
    pass


@bp.route('/<bid>/loads/<lid>', methods=["PUT", "DELETE"])
def add_remove_load(bid, lid):
    pass
