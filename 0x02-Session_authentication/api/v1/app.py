#!/usr/bin/env python3
"""
Route module for the API
"""
import imp
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
# from api.v1.auth.auth import Auth
# from api.v1.auth.basic_auth import BasicAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
AUTH_TYPE = getenv('AUTH_TYPE')

# set up Authentication type based on env variable
if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif AUTH_TYPE == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()


@app.before_request
def before_request() -> str:
    """ Autherize before request
    """
    paths = ['/api/v1/status/', '/api/v1/unauthorized/',
             '/api/v1/forbidden/', '/api/v1/auth_session/login/']
    request.current_user = auth.current_user(request)
    if auth is None:
        pass
    elif not auth.require_auth(request.path, paths):
        pass
    elif auth.authorization_header(request) is None:
        cookie = auth.session_cookie(request)
        if cookie is None:
            abort(401)
        if auth.user_id_for_session_id(cookie) is None:
            abort(403)
    elif auth.current_user(request) is None:
        abort(403)
    else:
        pass


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Not authorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbiden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
