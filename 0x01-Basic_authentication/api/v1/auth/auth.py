#!/usr/bin/env python3

"""
Module implements authentication class/ features
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Class Implements authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks excluded_paths and returns a boolean"""
        return False

    def authorization_header(self, request=None) -> str:
        """Checks authorization header"""
        if request:
            auth = request.headers.get("Authorization", None)
            return auth
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Handles user"""
        return None
