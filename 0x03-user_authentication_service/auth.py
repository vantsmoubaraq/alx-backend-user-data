#!/usr/bin/env python3

"""Module implements authentication protocols
"""

import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bcrypt:
    """Encrypts password"""
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers new user if not exist"""
        pass
