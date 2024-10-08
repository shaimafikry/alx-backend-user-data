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
    """ the session login
    """
    user_email = request.form.get('email')
    if not user_email:
        return jsonify({"error": "email missing"}), 400

    user_password = request.form.get('password')
    if not user_password:
        return jsonify({"error": "password missing"}), 400

    # retur value is a list
    try:
        user_list = User.search({'email': user_email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not user_list:
        return jsonify({"error": "no user found for this email"}), 404

    for user in user_list:
        # Validate password
        if not user.is_valid_password(user_password):
            return jsonify({"error": "wrong password"}), 401

    # Create a new session for the user
    from api.v1.app import auth
    user = user_list[0]
    session_id = auth.create_session(user.id)
    # Set the session cookie
    user_json = user.to_json()
    response = jsonify(user_json)
    SESSION_NAME = os.getenv('SESSION_NAME')
    response.set_cookie(SESSION_NAME, session_id)

    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """ DELETE /auth_session/logout
    Return:
        - Empty dictionary if succesful
    """
    from api.v1.app import auth

    deleted = auth.destroy_session(request)

    if not deleted:
        abort(404)

    return jsonify({}), 200
