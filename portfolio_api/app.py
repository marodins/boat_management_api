from flask import Flask
from portfolio_api.boats.routes import bp as boatbp
from portfolio_api.users.routes import bp as userbp
from portfolio_api.loads.routes import bp as loadsbp
from portfolio_api.utils.errors import Halt, any_error


def app_create():
    app = Flask(__name__)

    app.register_blueprint(boatbp)
    app.register_blueprint(userbp)
    app.register_blueprint(loadsbp)

    app.register_error_handler(Halt, any_error)

    return app






