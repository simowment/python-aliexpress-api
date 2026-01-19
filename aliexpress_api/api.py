"""AliExpress API wrapper for Python

A simple Python wrapper for the AliExpress Open Platform API. This module allows
to get product information and affiliate links from AliExpress using the official
API in an easier way.
"""

from .sdk import setDefaultAppInfo
from . import models
from .mixins.affiliate import AffiliateMixin
from .mixins.dropshipping import DropshippingMixin
from .mixins.common import CommonMixin

class AliexpressApi(CommonMixin, AffiliateMixin, DropshippingMixin):
    """Provides methods to get information from AliExpress using your API credentials.

    Args:
        key (str): Your API key.
        secret (str): Your API secret.
        language (str): Language code. Defaults to EN.
        currency (str): Currency code. Defaults to USD.
        tracking_id (str): The tracking id for link generator. Defaults to None.
    """

    def __init__(self,
        key: str,
        secret: str,
        language: models.Language = models.Language.EN,
        currency: models.Currency = models.Currency.USD,
        tracking_id: str = None,
        app_signature: str = None,
        token: str = None,
        **kwargs):
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
        """Prepares common request parameters.
        
        Args:
            request: The API request object.
            **params: Additional parameters to set on the request.
        """
        request.app_signature = self._app_signature
        
        # Set common parameters on the request object if it has them
        for key, value in params.items():
            if hasattr(request, key):
                setattr(request, key, value)
        
        return request
