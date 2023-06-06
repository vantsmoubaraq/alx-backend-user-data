#!/usr/bin/env python3

"""Module implements a flask application
"""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def form():
    """returns payload of form"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
