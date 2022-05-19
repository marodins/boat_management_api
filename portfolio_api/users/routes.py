from flask import Blueprint

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('', methods=["GET"])
def get_all():
    # paginate
    # self-links
    # total count
    pass


@bp.route('/<uid>', methods=["GET", "PUT", "PATCH", "DELETE"])
def mod_get(uid):
    pass


@bp.route('/<uid>/boats/<bid>', methods=["PUT", "PATCH", "DELETE"])
def mod_user_boat(uid, bid):
    # put adds a boat to users boats
    pass




