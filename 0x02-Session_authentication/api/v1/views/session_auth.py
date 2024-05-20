#!/usr/bin/env python3
""" Module of Session Auth
"""
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, abort
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login():
    """ GET /api/v1/auth_session/login
    Return:
      - User object in json and set session cookie
    """
    email = request.form.get("email")
    if not email or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    pwd = request.form.get("password")
    if not pwd or len(pwd) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({"email": email})
        if len(users) == 0:
            return jsonify({"error": "no user found for this email"}), 404
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]
    if not user.is_valid_password(pwd):
        return jsonify({"error": "wrong password"}), 401
    else:
        from api.v1.app import auth
        sess_id = auth.create_session(user.id)
        res = jsonify(user.to_json())
        res.set_cookie(os.getenv('SESSION_NAME'), sess_id)
        return res


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def auth_session_logout():
    """ GET /api/v1/auth_session/logout
    Desc: Logout a user session
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    else:
        abort(404)
