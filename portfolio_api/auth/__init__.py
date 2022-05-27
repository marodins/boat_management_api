# auth
from portfolio_api import config
from authlib.integrations.flask_client import OAuth


oauth = OAuth()
oauth.register(
    config.AUTH0_NAME,
    client_id=config.AUTH0_CLIENT_ID,
    client_secret=config.AUTH0_CLIENT_SECRET,
    api_base_url=config.AUTH0_API_BASE_URL,
    authorize_url=f'{config.AUTH0_API_BASE_URL}/authorize',
    access_token_url=f'{config.AUTH0_ACCESS_TOKEN_URL}',
    server_metadata_url=config.AUTH0_SERVER_METADATA_URL,
    client_kwargs={
        "scope": "openid profile email"
    }
)