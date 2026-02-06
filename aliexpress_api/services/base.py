"""Base service class for AliExpress API services.

This module provides a base class for all API services, handling common
functionality like configuration, request preparation, and SDK initialization.
"""

from typing import Optional, TYPE_CHECKING

from ..sdk import setDefaultAppInfo
from .. import models

if TYPE_CHECKING:
    from ..sdk.api.base import RestApi


class BaseService:
    """Base class for all AliExpress API services.

    Attributes:
        _key: App key for API authentication.
        _secret: App secret for signature generation.
        _token: Optional access token for authenticated requests.
        _language: Default language for API responses.
        _currency: Default currency for prices.
        _tracking_id: Optional tracking ID for affiliate links.
    """

    def __init__(
        self,
        key: str,
        secret: str,
        language: models.Language = models.Language.EN,
        currency: models.Currency = models.Currency.USD,
        tracking_id: Optional[str] = None,
        token: Optional[str] = None,
    ):
        """Initialize the base service.

        Args:
            key: App key for API authentication.
            secret: App secret for signature generation.
            language: Default language for API responses.
            currency: Default currency for prices.
            tracking_id: Optional tracking ID for affiliate links.
            token: Optional access token for authenticated requests.
        """
        self._key = key
        self._secret = secret
        self._language = language
        self._currency = currency
        self._tracking_id = tracking_id
        self._token = token

        # Initialize SDK with app credentials
        setDefaultAppInfo(key, secret)

    def _prepare_request(self, request: "RestApi", **params) -> "RestApi":
        """Prepare a request with common parameters.

        Args:
            request: The SDK request object.
            **params: Additional parameters to set on the request.

        Returns:
            The configured request object.
        """
        # Note: app_signature is not used in RestApi, it's an alias for something else
        # We'll skip setting it since it doesn't exist on RestApi objects

        for key, value in params.items():
            if hasattr(request, key) and value is not None:
                setattr(request, key, value)

        return request

    def _get_locale(self, country_code: Optional[str] = None) -> str:
        """Generate locale string from language and optional country code.

        Args:
            country_code: Optional country code (e.g., 'US').

        Returns:
            Locale string (e.g., 'en_US').
        """
        if country_code:
            return f"{str(self._language).lower()}_{country_code.upper()}"
        return f"{str(self._language).lower()}_US"
