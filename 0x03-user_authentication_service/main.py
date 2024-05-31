#!/usr/bin/env python3
""" Main
"""

import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """ Test Register User
    """
    url = 'http://localhost:5000/users'
    data = {"email": email, "password": password}
    res = requests.post(url, data=data)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "user created"}
    res = requests.post(url, data=data)
    assert res.status_code == 400
    assert res.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """ Log in with wrong pass password
    """
    url = 'http://localhost:5000/sessions'
    data = {"email": email, "password": password}
    res = requests.post(url, data=data)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """ Log in
    """
    url = 'http://localhost:5000/sessions'
    data = {"email": email, "password": password}
    res = requests.post(url, data=data)
    assert res.status_code == 200
    assert res.cookies.get('session_id')
    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    """ Get Profile when not logged in
    """
    url = 'http://localhost:5000/profile'
    res = requests.get(url)
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """ Get profile when logged in
    """
    url = 'http://localhost:5000/profile'
    res = requests.get(url, cookies={"session_id": session_id})
    assert res.status_code == 200
    assert res.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """ Logout
    """
    url = 'http://localhost:5000/sessions'
    res = requests.delete(url, cookies={"session_id": session_id})
    assert res.json() == {"message": "Bienvenue"}
    res = requests.delete(url, cookies={"session_id": session_id})
    assert res.status_code == 403


def reset_password_token(email: str) -> str:
    """ Reset Password token
    """
    url = 'http://localhost:5000/reset_password'
    res = requests.post(url, data={"email": "wrong_email"})
    assert res.status_code == 403
    res = requests.post(url, data={"email": email})
    assert res.json().get("email") == email
    return res.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Update password
    """
    url = 'http://localhost:5000/reset_password'
    data = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    res = requests.put(url, data=data)
    assert res.json() == {"email": email, "message": "Password updated"}
    res = requests.put(url, data={**data, "reset_token": "wrong_token"})
    assert res.status_code == 403


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, "wrong password")
    sess_id = log_in(EMAIL, PASSWD)
    profile_unlogged()
    profile_logged(sess_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_out(sess_id)
