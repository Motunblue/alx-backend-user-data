#!/usr/bin/env python3
""" Module of Auth
"""
from typing import List, TypeVar


class Auth:
    """ Class Auth
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Check if path require Authentification
        Return: True if path not in excluded_path else False
        """
        if not path or excluded_paths is None:
            return True
        if len(excluded_paths) == 0:
            return True
        if path[-1] == "*":
            for p in excluded_paths:
                if p.startswith(path[:-1]):
                    return True
        if path.strip()[-1] != "/":
            path = path + "/"
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """ Authorization Headers
        """
        None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current User
        """
        None

    def authorization_header(self, request=None) -> str:
        """ Validate API request
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)
