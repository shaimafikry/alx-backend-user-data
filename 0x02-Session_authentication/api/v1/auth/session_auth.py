#!/usr/bin/env python3
""" Module of auth class
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar
from uuid import uuid4


class SessionAuth(Auth):
    """ class auth"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates a session id for user_id"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
