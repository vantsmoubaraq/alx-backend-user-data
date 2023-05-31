#!/usr/bin/env python3

"""
Module implements basic authentication features
"""

from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
import base64
from models.user import User


class BasicAuth(Auth):
    """Class implements basic authentication features
    """
    def extract_base64_authorization_header(self, authorization_header:
                                            str) -> str:
        """Extract base64 part"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if authorization_header.split(" ")[0] != "Basic":
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        "Decode Base64"
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_bytes.decode("utf-8")
            return decoded_str
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Extracts user credentials"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        credentials = decoded_base64_authorization_header.split(":")
        return credentials[0], credentials[1]

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ return user instance
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            result = User.search({"email": user_email})
        except Exception:
            return None
        for user in result:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Basic authentication
        """
        header = self.authorization_header(request)
        if not header:
            return None
        value = self.extract_base64_authorization_header(header)
        if not value:
            return None
        decoded_str = self.decode_base64_authorization_header(value)
        if not decoded_str:
            return None
        email, pwd = self.extract_user_credentials(decoded_str)
        if not email or not pwd:
            return None
        return self.user_object_from_credentials(email, pwd)
