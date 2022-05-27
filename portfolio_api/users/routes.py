from flask import Blueprint, request
from db.google_db import DataAccess
from portfolio_api.utils.paginate import paginate
from portfolio_api.utils.utilities import make_self_link, make_res
bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('', methods=["GET"])
def get_all():
    users = DataAccess(kind='user', namespace='users')
    data = users.get_all()
    # create self links
    for user in data:
        for boat in user["boats"]:
            make_self_link(boat, request.base_url, segment=1, kind='boats')

    res_data = {
        "self": request.url,
        "users": data
    }
    return make_res(res_data, 200)





