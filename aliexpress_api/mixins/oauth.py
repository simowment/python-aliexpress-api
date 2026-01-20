"""OAuth authentication mixin for AliExpress API."""

import hashlib
import hmac
import time
import requests

from .. import models
from ..errors import ApiRequestException
from ..logging_config import get_logger

logger = get_logger("oauth")


class OAuthMixin:
    """Mixin providing OAuth authentication methods.
    
    This mixin adds OAuth token generation and refresh capabilities
    to the AliexpressApi class.
    """

    def generate_access_token(self, code: str, uuid: str = None) -> models.TokenResponse:
        """Generate an access token using the OAuth authorization code.
        
        Endpoint: POST /auth/token/create
        
        Args:
            code (str): OAuth code obtained from app callback URL. 
                        Note: Code expires after 3 minutes and can only be used once.
            uuid (str, optional): UUID parameter. Generally not needed and may cause errors.
        
        Returns:
            models.TokenResponse: Token response containing:
                - access_token (str): Access token for API calls
                - refresh_token (str): Token to refresh access when it expires
                - expires_in (int): Access token expiry time in seconds
                - refresh_expires_in (int): Refresh token expiry time in seconds
                - expire_time (int): Access token expiry timestamp (absolute)
                - refresh_token_valid_time (int): Refresh token expiry timestamp (absolute)
                - user_id, seller_id, account_id, user_nick, havana_id
                - account_platform, account, sp, locale
        
        Raises:
            ApiRequestException: If the request fails. Common error codes:
                - InvalidCode: Code expired, already used, or invalid
                - InvalidAppkey: App key is invalid
                - IncompleteSignature: Signature generation error
                - AUTH_TYPE_UNSUPPORTED: Authorization type not supported
        
        Example:
            >>> api = AliexpressApi(KEY, SECRET)
            >>> token = api.generate_access_token(code="oauth_code_from_callback")
            >>> print(token.access_token)
            >>> print(f"Expires in {token.expires_in} seconds")
        """
        return self._oauth_request(code=code, uuid=uuid)

    def refresh_access_token(self, refresh_token: str) -> models.TokenResponse:
        """Refresh an expired access token using the refresh token.
        
        Endpoint: POST /auth/token/refresh
        
        Use this method when the access_token has expired but refresh_token is still valid.
        Check refresh_expires_in > 0 to verify refresh is possible.
        
        Args:
            refresh_token (str): Refresh token obtained from generate_access_token().
        
        Returns:
            models.TokenResponse: New token response containing:
                - access_token (str): New access token for API calls
                - refresh_token (str): New refresh token (may be updated)
                - expires_in (int): New access token expiry time in seconds
                - refresh_expires_in (int): Refresh token expiry time in seconds
                - expire_time (int): Access token expiry timestamp (absolute)
                - refresh_token_valid_time (int): Refresh token expiry timestamp (absolute)
                - user_id, seller_id, account_id, user_nick, havana_id
                - account_platform, account, sp, locale
        
        Raises:
            ApiRequestException: If the request fails. Common error codes:
                - IllegalRefreshToken: Refresh token is invalid or expired
                - IllegalAccessToken: Access token is invalid
                - AUTH_TYPE_UNSUPPORTED: Authorization type not supported
        
        Example:
            >>> # When access token expires, refresh it
            >>> new_token = api.refresh_access_token(refresh_token=old_token.refresh_token)
            >>> print(new_token.access_token)
        """
        return self._oauth_request(refresh_token=refresh_token)

    def _oauth_request(
        self, 
        code: str = None, 
        uuid: str = None, 
        refresh_token: str = None
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

        # Generate HMAC-SHA256 signature (matching official IOP SDK)
        sorted_keys = sorted(params.keys())
        params_str = "".join(f"{k}{params[k]}" for k in sorted_keys)
        sign_string = api_path + params_str
        
        signature = hmac.new(
            self._secret.encode("utf-8"),
            sign_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest().upper()

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

