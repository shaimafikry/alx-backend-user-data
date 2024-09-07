#!/usr/bin/env python3
""" Module of auth class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ class of Auth"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ bool function"""
        if not path:
            return True
        if not excluded_paths or len(excluded_paths) == 0:
            return True
        if not path.endswith('/'):
            path += '/'
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """ header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user"""
        return None
