#!/usr/bin/env python3

"""Module implements authentication protocols
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


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
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            pass
        if user and user.email == email:
            raise ValueError(f"User {email} already exists")
        else:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)
