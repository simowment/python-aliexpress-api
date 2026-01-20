"""OAuth token response models for AliExpress API.

Endpoints:
    - POST /auth/token/create - Generate access token from OAuth code
    - POST /auth/token/refresh - Refresh expired access token
"""

from dataclasses import dataclass
from typing import Optional
from .base import BaseModel


@dataclass
class TokenResponse(BaseModel):
    """Response from OAuth token generation (/auth/token/create) or refresh (/auth/token/refresh).

    This model represents the response from both endpoints as they return the same structure.

    Attributes:
        access_token (str): Access token for making authenticated API calls.
        refresh_token (str): Refresh token to obtain new access token when it expires.
            Use when refresh_expires_in > 0.
        expires_in (int): Access token expiry time in seconds (relative time).
        refresh_expires_in (int): Refresh token expiry time in seconds (relative time).
        expire_time (int): Access token expiry timestamp in milliseconds (absolute time).
        refresh_token_valid_time (int): Refresh token expiry timestamp in milliseconds (absolute time).
        account_id (str): Account ID. May be null if account_platform=seller_center.
        seller_id (str): Seller ID.
        user_id (str): User ID.
        user_nick (str): User nickname.
        havana_id (str): Havana ID.
        account_platform (str): Account platform (e.g., 'ae', 'seller_center').
        account (str): User account (login user email/username).
        sp (str): Authorization platform.
        locale (str): User's locale/language setting.

    Example:
        >>> token = api.generate_access_token(code="oauth_code")
        >>> print(f"Access token: {token.access_token}")
        >>> print(f"Expires in: {token.expires_in} seconds")
        >>> # Store refresh_token for later use
        >>> save_to_db(token.refresh_token, token.refresh_token_valid_time)
    """
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    refresh_expires_in: Optional[int] = None
    expire_time: Optional[int] = None
    refresh_token_valid_time: Optional[int] = None
    account_id: Optional[str] = None
    seller_id: Optional[str] = None
    user_id: Optional[str] = None
    user_nick: Optional[str] = None
    havana_id: Optional[str] = None
    account_platform: Optional[str] = None
    account: Optional[str] = None
    sp: Optional[str] = None
    locale: Optional[str] = None

