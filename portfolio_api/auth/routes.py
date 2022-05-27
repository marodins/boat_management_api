from flask import Blueprint, request, render_template, url_for
from portfolio_api.auth import oauth
from db.google_db import DataAccess

bp = Blueprint('welcome', __name__, url_prefix='/',
               template_folder='../../templates')


@bp.route('', methods=["GET"])
def welcome():
    if request.method == 'GET':
        return render_template('welcome.html')


@bp.route('authorize', methods=["GET"])
def auth_user():
    auth0 = oauth.create_client('auth0')
    return auth0.authorize_redirect(
        redirect_uri=url_for('welcome.profile', _external=True)
    )


@bp.route('profile', methods=["GET", "POST"])
def profile():
    user = DataAccess(kind='user', namespace='users')
    token = oauth.auth0.authorize_access_token()
    id_token = token["id_token"]
    name = token.get('userinfo', None)
    sub = name.get('sub', None)
    if name:
        name = name.get('nickname', None)

    # check if user already registered, otherwise add to db
    res = list(user.get_all_filtered([('sub', '=', sub)]))
    if not res:
        data = {
            "name": name,
            "sub": sub,
            "boats": list()
        }
        user.add_entity(data)

    return render_template(
        'profile.html',
        id_token=id_token,
        sub=sub,
        name=name
    )

