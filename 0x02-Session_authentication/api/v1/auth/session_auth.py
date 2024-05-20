#!/usr/bin/env python3
""" Module of Session Auth
"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request
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


class SessionAuth(Auth):
    """ Session Authentification
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create session
        """
        if type(user_id) != str:
            return None
        sess_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[sess_id] = user_id
        return sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Return userId using the session id
        """
        if type(session_id) != str:
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie)
        try:
            user = User.get(user_id)
            return user
        except Exception:
            return None
