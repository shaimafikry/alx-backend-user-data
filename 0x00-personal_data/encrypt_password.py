#!/usr/bin/env python3
"""
encrypt file
"""

import logging
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.

    Args:
    - password: The password string to hash.

    Returns:
    - The salted, hashed password as a byte string.
    """
    salt: bytes = bcrypt.gensalt()
    hashed_password: bytes = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates if the provided password matches the hashed password.

    Args:
    - hashed_password: The hashed password as bytes.
    - password: The plain-text password to validate.

    Returns:
    - True if the password matches the hash, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
