from flask import Blueprint

bp = Blueprint('boats', __name__, url_prefix='/boats')


@bp.route('', methods=["GET", "POST"])
def add_get_boat():
    # paginate
    # self-links
    # total count

    pass


@bp.route('/<bid>', methods=["GET", "PUT", "PATCH", "DELETE"])
def get_mod_boat(bid):
    # modifying a boat that belongs to a user required jwt
    pass


@bp.route('/<bid>/loads/<lid>', methods=["PUT", "DELETE"])
def add_remove_load(bid, lid):
    pass
