from flask import Flask
from portfolio_api.boats.routes import bp as boatbp
from portfolio_api.users.routes import bp as userbp
from portfolio_api.loads.routes import bp as loadsbp
from portfolio_api.auth.routes import bp as authbp
from portfolio_api.utils.errors import Halt, any_error
from portfolio_api.config import *


def app_create():
    app = Flask(__name__, static_folder='../static', static_url_path='/static')
    app.secret_key = APP_SECRET
    app.register_blueprint(boatbp)
    app.register_blueprint(userbp)
    app.register_blueprint(loadsbp)
    app.register_blueprint(authbp)

    app.register_error_handler(Halt, any_error)

    from portfolio_api.auth import oauth
    oauth.init_app(app)

    return app






