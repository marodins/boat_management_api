from flask import Blueprint

bp = Blueprint('loads', __name__, url_prefix='/loads')


@bp.route('', methods=["GET", "POST"])
def add_get_loads():
    # paginate
    # self-links
    # total count
    pass


@bp.route('/<lid>', methods=["GET", "PUT", "PATCH", "DELETE"])
def specific_load(lid):
    pass
