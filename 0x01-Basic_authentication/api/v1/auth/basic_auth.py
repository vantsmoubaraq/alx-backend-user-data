#!/usr/bin/env python3

"""
Module implements basic authentication features
"""

from flask import request
from typing import List
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """Class implements basic authentication features
    """
    def extract_base64_authorization_header(self, authorization_header:
                                            str) -> str:
        """Encode in base64"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if authorization_header.split(" ")[0] != "Basic":
            return None
        return authorization_header.split(" ")[1]
