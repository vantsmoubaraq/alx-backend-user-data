#!/usr/bin/env python3

"""
Module implements authentication class/ features
"""

from flask import request
from typing import List, TypeVar
import re
from os import getenv, environ


class Auth:
    """Class Implements authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks excluded_paths and returns a boolean"""
        if not path or not excluded_paths:
            return True
        if path:
            if path.endswith("*"):
                for item in excluded_paths:
                    if path[:-1] in item:
                        path = item
            elif not path.endswith("/"):
                path = path + "/"
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Checks authorization header"""
        if request:
            auth = request.headers.get("Authorization", None)
            return auth
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Handles user"""
        return None

    def session_cookie(self, request=None):
        """returns value of a cookie from a dictionary"""
        if request is None:
            return None
        try:
            _my_session_id = request.cookies.get("_my_session_id")
            environ["SESSION_NAME"] =  _my_session_id
            return _my_session_id 
        except Exception:
            pass
        
