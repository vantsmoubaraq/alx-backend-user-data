#!/usr/bin/env python3

"""
Module implements authentication class/ features
"""

import requests


class Auth:
    """Class Implements authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks excluded_paths and returns a boolean"""
        pass

    def authorization_header(self, request=None) -> str:
        """Checks authorization header"""
        pass

    def current_user(self, request=None) -> TypeVar('User'):
        """Handles user"""
        pass
