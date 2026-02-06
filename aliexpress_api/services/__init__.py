"""Service classes for AliExpress API.

This module provides composition-based services for the AliExpress API,
replacing the mixin-based approach for better modularity and testability.
"""

from .oauth import OAuthService
from .dropshipping import DropshippingService
from .affiliate import AffiliateService
from .common import CommonService

__all__ = ["OAuthService", "DropshippingService", "AffiliateService", "CommonService"]
