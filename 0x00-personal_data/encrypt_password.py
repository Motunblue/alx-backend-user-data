#!/usr/bin/env python3
"""Encrypt Password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hash Password"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Check if a password is valid password
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
