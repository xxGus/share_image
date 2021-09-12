from collections import namedtuple
from functools import wraps

from bson import ObjectId
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from .http_reponses import error

def data_required(params: set):
    def decorator(fun):
        def wrapper(*args, **kwargs):
            if (
                not request.content_type
                or "application/json" not in request.content_type
            ):
                return error("missing data or Content-Type")

            data = request.json
            if not data:
                return error("missing data")

            if params:
                diff = params.difference(set(data.keys()))
                if len(diff) > 0:
                    return error("missing params: {}".format(",".join(diff)))

            for key in data:
                if "_id" in key:
                    if not ObjectId.is_valid(data[key]):
                        return error("invalid param: {}".format(key))

                if data[key] == "" or data[key] is None:
                    return error("invalid param: {}".format(key))

            return fun(*args, **kwargs)

        return wrapper

    return decorator


def perm_required(role):
    def decorator(fun):
        @jwt_required
        def wrapper(*args, **kwargs):
            session_data = get_jwt_identity()
            
            if not session_data["permissions"]:
                return error("operation not permitted.", 403)

            permissions = session_data["permissions"]
            if role not in permissions:
                return error("operation not permitted.", 403)
            return fun(*args, **kwargs)

        return wrapper

    return decorator


JwtData = namedtuple("JwtData", ["user_id", "permissions"])

def application_jwt_required(fn):
    """
    A decorator to protect a Flask endpoint.
    Works exactly like `flask_jwt_extended.jwt_required`,
    but passes the jwt's data as params to the wrapped function.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        jwt_data = get_jwt_identity()

        if not jwt_data:
            return error("JWT required")

        user_id = jwt_data.get("user_id")
        permissions = jwt_data.get("permissions")

        jwt = JwtData(user_id, permissions)
        return fn(jwt_data=jwt, *args, **kwargs)

    return wrapper