#!/usr/bin/env python3
""" Module of auth class
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """ class of Auth"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ bool function"""
        if not path:
            return True
        if not excluded_paths or len(excluded_paths) == 0:
            return True
        for p in excluded_paths:
            if p.endswith('*'):
                last = p.split('/')[-1].replace('*', '')
                path_split = path.split('/')
                if path.endswith('/'):
                    path_compare = path_split[-2].startswith(last)
                else:
                    path_compare = path_split[-1].startswith(last)
                if path_compare:
                    return False
                else:
                    return True
        if not path.endswith('/'):
            path += '/'
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """ header"""
        if request is None:
            return None
        head = request.headers.get('Authorization')
        if not head:
            return None
        return head

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user"""
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request"""
        if request is None:
            return None
        cookie_name = os.getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(cookie_name)
