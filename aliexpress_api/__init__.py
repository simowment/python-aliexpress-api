"""AliExpress API wrapper for Python

A Python wrapper for the AliExpress Open Platform API, supporting:
- Affiliate marketing operations
- Dropshipping operations
- OAuth authentication

Example:
    >>> from aliexpress_api import AliexpressApi, models

    # New composition-based API (recommended)
    >>> api = AliexpressApi(KEY, SECRET, tracking_id="YOUR_TRACKING_ID")
    >>> product = api.dropshipping.get_ds_product('1005001234567890', 'US')
    >>> links = api.affiliate.get_affiliate_links(['https://aliexpress.com/item/123.html'])

    # Old mixin-based API (still supported)
    >>> product = api.get_ds_product('1005001234567890', 'US')
    >>> links = api.get_affiliate_links(['https://aliexpress.com/item/123.html'])
"""

__author__ = "Sergio Abad"

# Main API class
from .api import AliexpressApi

# Models
from . import models

# Logging configuration
from .logging_config import set_debug_mode, is_debug_mode

# New service classes (composition-based API)
from .services import (
    OAuthService,
    CommonService,
    AffiliateService,
    DropshippingService,
)

# Keep mixins for backward compatibility
from .mixins import (
    OAuthMixin,
    CommonMixin,
    AffiliateMixin,
    DropshippingMixin,
)

__all__ = [
    # Main class
    "AliexpressApi",
    # Models
    "models",
    # Services (new composition-based API)
    "OAuthService",
    "CommonService",
    "AffiliateService",
    "DropshippingService",
    # Logging
    "set_debug_mode",
    "is_debug_mode",
    # Mixins (deprecated, kept for backward compatibility)
    "OAuthMixin",
    "CommonMixin",
    "AffiliateMixin",
    "DropshippingMixin",
]
