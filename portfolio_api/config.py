import os


AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE')
APP_SECRET = os.getenv('APP_SECRET')
AUTH0_CONNECTION = os.getenv('CONNECTION')
AUTH0_SERVER_METADATA_URL = f'https://{os.getenv("AUTH0_DOMAIN")}' \
                            f'/.well-known/openid-configuration'
AUTH0_NAME = "auth0"
AUTH0_ACCESS_TOKEN_URL = f'https://{AUTH0_DOMAIN}/oauth/token'
AUTH0_API_BASE_URL = f'https://{AUTH0_DOMAIN}'
