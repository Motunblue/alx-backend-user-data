#!/usr/bin/env python3
""" Module of Basic Auth
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """ Basic Authentification
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ Extract Base64 Authorization from header
        """
        if authorization_header is None or type(authorization_header) != str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Decode Base64 authorization header
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            credentials = base64.b64decode(base64_authorization_header)
            return credentials.decode('utf-8')
        except (ValueError, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> (str, str):
        """ Extract user credentials
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) != str:
            return None, None
        if decoded_base64_authorization_header.find(":") == -1:
            return None, None
        usr, pwd = decoded_base64_authorization_header.split(":")
        return usr, pwd

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
            ) -> TypeVar('User'):
        """ Get user object from credentials
        """
        if type(user_email) != str or type(user_pwd) != str:
            return None
        user = User.search({'email': user_email})
        if len(user) == 0:
            return None
        if user[0].is_valid_password(user_pwd):
            return user[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user
        """
        auth_header = self.authorization_header(request)
        base64_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(base64_token)
        email, pwd = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, pwd)
