"""AliExpress API wrapper for Python.

This module provides a high-level interface to the AliExpress Open Platform API,
supporting affiliate marketing, dropshipping, and OAuth authentication.

Example:
    >>> from aliexpress_api import AliexpressApi, models, set_debug_mode
    >>>
    >>> # Enable debug logging (optional)
    >>> set_debug_mode(True)
    >>>
    >>> # Initialize the API
    >>> api = AliexpressApi(
    ...     key="your_app_key",
    ...     secret="your_app_secret",
    ...     language=models.Language.EN,
    ...     currency=models.Currency.USD,
    ...     tracking_id="your_tracking_id"
    ... )
    >>>
    >>> # Generate affiliate links
    >>> links = api.get_affiliate_links(["https://aliexpress.com/item/123.html"])
"""

from .sdk import setDefaultAppInfo
from . import models
from .mixins.affiliate import AffiliateMixin
from .mixins.dropshipping import DropshippingMixin
from .mixins.common import CommonMixin
from .mixins.oauth import OAuthMixin


class AliexpressApi(OAuthMixin, CommonMixin, AffiliateMixin, DropshippingMixin):
    """Main API class providing access to all AliExpress API functionality.

    This class combines functionality from multiple mixins:
    - OAuthMixin: Token generation and refresh
    - CommonMixin: Common API operations
    - AffiliateMixin: Affiliate marketing operations
    - DropshippingMixin: Dropshipping operations

    Attributes:
        _key: App key for API authentication
        _secret: App secret for signature generation
        _tracking_id: Tracking ID for affiliate links
        _language: Default language for API responses
        _currency: Default currency for prices
        _app_signature: Optional app signature
        _token: Optional access token for authenticated requests
        categories: Cached categories list
    """

    def __init__(
        self,
        key: str,
        secret: str,
        language: models.Language = models.Language.EN,
        currency: models.Currency = models.Currency.USD,
        tracking_id: str = None,
        app_signature: str = None,
        token: str = None,
        **kwargs
    ):
        """Initialize the AliExpress API client.

        Args:
            key: Your AliExpress app key
            secret: Your AliExpress app secret
            language: Default language for API responses (default: EN)
            currency: Default currency for prices (default: USD)
            tracking_id: Your affiliate tracking ID (required for affiliate links)
            app_signature: Optional app signature
            token: Optional access token for authenticated requests
            **kwargs: Additional arguments (reserved for future use)
        """
        self._key = key
        self._secret = secret
        self._tracking_id = tracking_id
        self._language = language
        self._currency = currency
        self._app_signature = app_signature
        self._token = token
        self.categories = None
        setDefaultAppInfo(self._key, self._secret)

    def _prepare_request(self, request, **params):
        """Prepare a request with common parameters.

        Args:
            request: The SDK request object
            **params: Additional parameters to set on the request

        Returns:
            The configured request object
        """
        request.app_signature = self._app_signature
        for key, value in params.items():
            if hasattr(request, key):
                setattr(request, key, value)
        return request
