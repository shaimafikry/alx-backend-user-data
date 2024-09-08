#!/usr/bin/env python3
""" Module of session auth views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login',
                 methods=['POST'], strict_slashes=False)
def login() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    user_email = request.form.get('email')
    if not user_email:
        return jsonify({"error": "email missing"}), 400

    user_password = request.form.get('password')
    if not user_password:
        return jsonify({"error": "password missing"}), 400

    # retur value is a list
    user_list = User.search({'email': user_email})
    if not user or len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = user_list[0]

    # Validate password
    if not user.is_valid_password(user_password):
        return jsonify({"error": "wrong password"}), 401

    # Create a new session for the user
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    if not session_id:
        return jsonify({"error": "could not create session"}), 500

    # Set the session cookie
    response = jsonify(user.to_json())
    session_name = os.getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(session_name, session_id)

    return response
