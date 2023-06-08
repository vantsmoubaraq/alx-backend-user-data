#!/usr/bin/env python3

"""Module implements SessionAuth class"""

from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """Class implements session authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates session id"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns user id based on session id"""
        if session_id is None:
            return None
        if type(session_id) is not str:
            return None
        try:
            return self.user_id_by_session_id[session_id]
        except Exception:
            pass
    
    def current_user(self, request=None):
        """returns a User instance based on a cookie value"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)
        return user
    
