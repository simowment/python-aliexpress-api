"""OAuth service for AliExpress API.

This module provides OAuth authentication methods for the AliExpress API.
"""

import hashlib
import hmac
import time
import requests
from typing import Optional

from .base import BaseService
from .. import models
from ..errors import ApiRequestException
from ..logging_config import get_logger

logger = get_logger("oauth")


class OAuthService(BaseService):
    """Service providing OAuth authentication methods.

    Example:
        >>> from aliexpress_api import AliexpressApi
        >>> api = AliexpressApi(KEY, SECRET)
        >>> token = api.oauth.generate_access_token(code="oauth_code_from_callback")
        >>> print(token.access_token)
    """

    def generate_access_token(
        self, code: str, uuid: Optional[str] = None
    ) -> models.TokenResponse:
        """Generate an access token using the OAuth authorization code.

        Endpoint: POST /auth/token/create

        Args:
            code: OAuth code obtained from app callback URL.
                  Note: Code expires after 3 minutes and can only be used once.
            uuid: Optional UUID parameter. Generally not needed and may cause errors.

        Returns:
            TokenResponse containing access_token, refresh_token, expires_in, etc.

        Raises:
            ApiRequestException: If the request fails.
        """
        return self._oauth_request(code=code, uuid=uuid)

    def refresh_access_token(self, refresh_token: str) -> models.TokenResponse:
        """Refresh an expired access token using the refresh token.

        Endpoint: POST /auth/token/refresh

        Args:
            refresh_token: Refresh token obtained from generate_access_token().

        Returns:
            TokenResponse with new access token and possibly new refresh token.

        Raises:
            ApiRequestException: If the request fails.
        """
        return self._oauth_request(refresh_token=refresh_token)

    def _oauth_request(
        self,
        code: Optional[str] = None,
        uuid: Optional[str] = None,
        refresh_token: Optional[str] = None,
    ) -> models.TokenResponse:
        """Internal method to make OAuth token requests.

        Handles both token generation and token refresh using HMAC-SHA256 signature.
        """
        if refresh_token:
            url = "https://api-sg.aliexpress.com/rest/auth/token/refresh"
            api_path = "/auth/token/refresh"
        else:
            url = "https://api-sg.aliexpress.com/rest/auth/token/create"
            api_path = "/auth/token/create"

        # Build parameters
        params = {
            "app_key": self._key,
            "timestamp": str(int(time.time() * 1000)),
            "sign_method": "sha256",
        }

        if refresh_token:
            params["refresh_token"] = refresh_token
        else:
            params["code"] = code
            if uuid:
                params["uuid"] = uuid

        # Generate HMAC-SHA256 signature
        sorted_keys = sorted(params.keys())
        params_str = "".join(f"{k}{params[k]}" for k in sorted_keys)
        sign_string = api_path + params_str

        signature = (
            hmac.new(
                self._secret.encode("utf-8"),
                sign_string.encode("utf-8"),
                hashlib.sha256,
            )
            .hexdigest()
            .upper()
        )

        logger.debug(f"OAuth request to {api_path}")
        logger.debug(f"Params: {params}")
        logger.debug(f"Sign string: {sign_string}")
        logger.debug(f"Signature: {signature}")

        params["sign"] = signature

        try:
            response = requests.post(url, data=params)
            logger.debug(f"OAuth response: {response.text}")
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            raise ApiRequestException(f"OAuth request failed: {str(e)}") from e

        if "error_response" in data:
            error = data["error_response"]
            error_code = error.get("code", "Unknown")
            error_msg = error.get("msg", "Unknown error")
            raise ApiRequestException(f"{error_code}: {error_msg}")

        # Extract token data from response
        token_data = data
        if "access_token" not in data:
            for key in ["token_response", "result", "data"]:
                if key in data and isinstance(data[key], dict):
                    token_data = data[key]
                    break

        return models.TokenResponse.from_dict(token_data)
