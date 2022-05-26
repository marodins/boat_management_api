from flask import Blueprint, request, g
from portfolio_api.utils.errors import Halt
from db.google_db import DataAccess
from portfolio_api.utils.utilities import make_res, make_self_link
from portfolio_api.utils.closures import paginate

bp = Blueprint('loads', __name__, url_prefix='/loads')


@bp.route('', methods=["GET", "POST"])
@paginate('load', 'loads', DataAccess)
def add_get_loads():
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
        data = g.data["data"]
        next_link = g.data["next_link"]
        count = g.data["total_count"]
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
def specific_load(lid):
    pass
