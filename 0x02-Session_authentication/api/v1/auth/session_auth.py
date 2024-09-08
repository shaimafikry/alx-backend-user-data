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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """return user id based on sesion"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """returns a User instance based on a cookie value"""
        id_session = self.session_cookie(request)
        user_id = self.user_id_for_session_id(id_session)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """deletes the user session / logout"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
