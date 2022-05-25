from flask import Blueprint, request
from portfolio_api.utils.errors import Halt
from db.google_db import DataAccess
from portfolio_api.utils.utilities import make_res, make_self_link

bp = Blueprint('loads', __name__, url_prefix='/loads')


@bp.route('', methods=["GET", "POST"])
def add_get_loads():
    # paginate
    # self-links
    # total count
    load = DataAccess(kind="load", namespace="loads")
    res = None
    if request.method == 'POST':

        data = request.json
        try:
            load_type = data["type"]
            weight = data["weight"]
            length = data["length"]

            load.add_entity({
                "type": load_type,
                "weight": weight,
                "length": length,
                "boat": None
            })
            load.entity["id"] = load.entity.id
            make_self_link(load.entity, request.base_url)
            res = make_res(load.entity, 201)
        except KeyError:
            raise Halt('missing attribute', 400)

    if request.method == 'GET':
        pass

    return res


@bp.route('/<lid>', methods=["GET", "PUT", "PATCH", "DELETE"])
def specific_load(lid):
    pass
