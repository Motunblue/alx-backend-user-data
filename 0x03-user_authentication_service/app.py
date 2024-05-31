#!/usr/bin/env python3
""" Flask App
"""
from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """Retrieve home """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_users():
    """ Register Users """
    try:
        user = AUTH.register_user(request.form.get("email"),
                                  request.form.get("password"))
        return jsonify({"email": f"{user.email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
