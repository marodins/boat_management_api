from functools import wraps
import requests
from jose import jwt
from flask import request, g
from portfolio_api.utils.errors import Halt
from portfolio_api import config


def get_rsa(webkeys, unver):
    """ find matching key and collect key information """
    if unver["alg"] != "RS256":
        raise Halt("incorrect algorithm", 401)

    for key in webkeys["keys"]:
        if key["kid"] == unver["kid"]:
            return {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    raise Halt("no key match found", 401)


def validating(errors=False):
    def validation(func):

        @wraps(func)
        def validate(*args, **kwargs):

            error = None
            try:
                auth = request.headers.get('Authorization')
                [bearer, token] = auth.split()
                if "bearer" != bearer.lower():
                    error = Halt("incorrect formatting of auth header", 401)
                res = requests.get(config.AUTH0_API_BASE_URL +
                                   "/.well-known/jwks.json")

                unverified = jwt.get_unverified_header(token)

                rsa_key = get_rsa(res.json(), unverified)

                payload = jwt.decode(
                    token,
                    rsa_key,
                    audience=config.AUTH0_CLIENT_ID,
                    algorithms=["RS256"],
                    issuer=f"https://{config.AUTH0_DOMAIN}/"
                )
                # will only be set if no exceptions raised prior
                # indicating successful payload retrieval
                g.jwt_payload = payload
                g.error = None
            except jwt.ExpiredSignatureError:
                error = Halt("expired token", 401)
            except jwt.JWTClaimsError as e:
                error = Halt(str(e), 401)
            except KeyError:
                error = Halt("no authorization header provided", 401)
            except ValueError:
                error = Halt("token or 'bearer' missing ", 401)
            except AttributeError:
                error = Halt("token is missing", 401)
            except Halt as res_error:
                error = res_error
            except Exception as e:
                error = Halt(str(e), 401)
            finally:
                if error and errors:
                    raise error
                if error and not errors:
                    g.error = error

            return func(*args, **kwargs)

        return validate
    return validation

