#!/usr/bin/env python3

"""Module implements authentication protocols
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """Encrypts password"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def _generate_uuid() -> str:
    """Generates uuids"""
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """Credentials validation
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode(), user.hashed_password):
                return True
        except Exception:
            pass
        return False

    def create_session(self, email: str) -> str:
        """ Creates session id
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id
        except Exception:
            pass

    def get_user_from_session_id(self, session_id: str) -> User:
        """get_user_from_session_id
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return user
        except Exception:
            pass
    
    def destroy_session(self, user_id: int) -> None:
        """Destroys session"""
        try:
            user = self._db.find_user_by(id=user_id)
            if user:
                user.session_id = None
        except Exception:
            pass
