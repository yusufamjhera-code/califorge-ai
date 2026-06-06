"""
Firebase Authentication & token verification.

Provides dependency injection for FastAPI routes to verify
Firebase ID tokens and extract authenticated user information.
"""

from __future__ import annotations

import logging
from typing import Optional

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import Settings, get_settings

logger = logging.getLogger(__name__)

# HTTP Bearer scheme for extracting tokens from Authorization header
bearer_scheme = HTTPBearer(auto_error=False)


def initialize_firebase(settings: Optional[Settings] = None) -> None:
    """Initialize the Firebase Admin SDK.
    
    Since we are now using google.oauth2.id_token for local verification,
    we no longer need to initialize the firebase_admin SDK for token checking.
    This function is kept for backward compatibility with main.py lifespan.
    """
    logger.info("🔐 Firebase verification initialized (using google-auth)")


def verify_firebase_token(token: str) -> dict:
    """Verify a Firebase ID token and return the decoded claims.

    Args:
        token: The Firebase ID token string.

    Returns:
        Decoded token claims dict containing uid, email, etc.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    settings = get_settings()
    try:
        request = google_requests.Request()
        decoded = id_token.verify_firebase_token(
            token, 
            request, 
            audience=settings.FIREBASE_PROJECT_ID
        )
        return decoded
    except ValueError as exc:
        logger.error("Token verification failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as exc:
        logger.error("Unexpected error verifying token: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> dict:
    """FastAPI dependency that extracts and verifies the current user.

    Reads the Bearer token from the Authorization header, verifies it
    with Firebase, and returns the decoded user claims.

    Returns:
        Dict with at least 'uid', 'email', and other Firebase claims.

    Raises:
        HTTPException 401: If no token is provided or token is invalid.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Provide a Bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    decoded = verify_firebase_token(credentials.credentials)
    
    # Ensure 'uid' exists, as the rest of the backend relies on it.
    if "uid" not in decoded and "sub" in decoded:
        decoded["uid"] = decoded["sub"]
        
    return decoded


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> Optional[dict]:
    """FastAPI dependency for optional authentication.

    Returns decoded user claims if a valid token is provided,
    or None if no token is present. Useful for endpoints that
    behave differently for authenticated vs anonymous users.
    """
    if credentials is None:
        return None

    try:
        decoded = verify_firebase_token(credentials.credentials)
        if "uid" not in decoded and "sub" in decoded:
            decoded["uid"] = decoded["sub"]
        return decoded
    except HTTPException:
        return None


async def get_admin_user(
    current_user: dict = Depends(get_current_user),
) -> dict:
    """FastAPI dependency that requires admin privileges.

    Checks for the 'admin' custom claim on the Firebase token.

    Returns:
        Decoded user claims if the user is an admin.

    Raises:
        HTTPException 403: If the user does not have admin privileges.
    """
    if not current_user.get("admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required.",
        )
    return current_user
