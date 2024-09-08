#!/usr/bin/env python3
""" Module of auth class
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar


class SessionAuth(Auth):
    """ class auth"""
    pass
