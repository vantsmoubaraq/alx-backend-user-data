#!/usr/bin/env python3

"""Module implements a flask application
"""

from flask import Flask, jsonify, request, abort, make_response
from flask import redirect, url_for
from auth import Auth
import json

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def form():
    """returns payload of form"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """registers a user"""
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """login function"""
    email = request.form.get("email")
    password = request.form.get("password")

    validity = AUTH.valid_login(email, password)

    if validity:
        session_id = AUTH.create_session(email)
        response = make_response({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


@app.route("/logout", methods=["DELETE"])
def logout():
    """Logs user out"""
    session_id = request.cookies.get("session_id")
    try:
        user = self._db.find_user_by(session_id=session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect('/')
        else:
            abort(403)
    except Exception:
        pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
