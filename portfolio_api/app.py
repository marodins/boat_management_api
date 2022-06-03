from flask import Flask
from portfolio_api.utils.errors import Halt, any_error, method_error
from dotenv import load_dotenv
from portfolio_api.config import *


def app_create(env_config=os.getenv('FLASK_ENV', None)):
    app = Flask(__name__, static_folder='../static', static_url_path='/static')
    # if development load env; production will use app.yaml
    if env_config == 'development':
        path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(path)

    app.secret_key = APP_SECRET

    from portfolio_api.boats.routes import bp as boatbp
    from portfolio_api.users.routes import bp as userbp
    from portfolio_api.loads.routes import bp as loadsbp
    from portfolio_api.auth.routes import bp as authbp
    app.register_blueprint(boatbp)
    app.register_blueprint(userbp)
    app.register_blueprint(loadsbp)
    app.register_blueprint(authbp)

    app.register_error_handler(Halt, any_error)
    app.register_error_handler(405, method_error)

    from portfolio_api.auth import oauth
    oauth.init_app(app)

    return app






