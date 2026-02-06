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
    >>> # New composition-based API (recommended)
    >>> product = api.dropshipping.get_ds_product('1005001234567890', 'US')
    >>> links = api.affiliate.get_affiliate_links(['https://aliexpress.com/item/123.html'])
    >>>
    >>> # Old mixin-based API (still supported for backward compatibility)
    >>> product = api.get_ds_product('1005001234567890', 'US')
    >>> links = api.get_affiliate_links(['https://aliexpress.com/item/123.html'])
"""

from typing import TYPE_CHECKING

from .services import OAuthService, CommonService, AffiliateService, DropshippingService
from . import models

if TYPE_CHECKING:
    from .services.base import BaseService


class AliexpressApi:
    """Main API class providing access to all AliExpress API functionality.

    This class uses composition to provide access to all API functionality
    through dedicated service objects. It also provides backward-compatible
    wrappers for the old mixin-based API.

    Attributes:
        oauth: OAuth authentication service
        common: Common API operations service
        affiliate: Affiliate marketing service
        dropshipping: Dropshipping service
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
        **kwargs,
    ):
        """Initialize the AliExpress API client.

        Args:
            key: Your AliExpress app key
            secret: Your AliExpress app secret
            language: Default language for API responses (default: EN)
            currency: Default currency for prices (default: USD)
            tracking_id: Your affiliate tracking ID (required for affiliate links)
            app_signature: Optional app signature (deprecated)
            token: Optional access token for authenticated requests
            **kwargs: Additional arguments (reserved for future use)
        """
        self._key = key
        self._secret = secret
        self._tracking_id = tracking_id
        self._language = language
        self._currency = currency
        self._token = token
        self._app_signature = app_signature

        # Initialize services using composition
        self.oauth = OAuthService(
            key=key,
            secret=secret,
            language=language,
            currency=currency,
            tracking_id=tracking_id,
            token=token,
        )

        self.common = CommonService(
            key=key,
            secret=secret,
            language=language,
            currency=currency,
            tracking_id=tracking_id,
            token=token,
        )

        self.affiliate = AffiliateService(
            key=key,
            secret=secret,
            language=language,
            currency=currency,
            tracking_id=tracking_id,
            token=token,
        )

        self.dropshipping = DropshippingService(
            key=key,
            secret=secret,
            language=language,
            currency=currency,
            tracking_id=tracking_id,
            token=token,
        )

    def __getattr__(self, name: str):
        """Provide backward compatibility for mixin-based API.

        Delegates attribute access to the appropriate service for methods
        that were previously provided by mixins.
        """
        # Map old method names to new service methods
        method_map = {
            # OAuth methods
            "generate_access_token": self.oauth.generate_access_token,
            "refresh_access_token": self.oauth.refresh_access_token,
            # Common methods
            "get_products_details": self.common.get_products_details,
            "get_categories": self.common.get_categories,
            "get_parent_categories": self.common.get_parent_categories,
            "get_child_categories": self.common.get_child_categories,
            "calculate_buyer_freight": self.common.calculate_buyer_freight,
            # Affiliate methods
            "get_affiliate_links": self.affiliate.get_affiliate_links,
            "get_hotproducts": self.affiliate.get_hotproducts,
            "get_products": self.affiliate.get_products,
            "smart_match_product": self.affiliate.smart_match_product,
            "get_order_list": self.affiliate.get_order_list,
            # Dropshipping methods
            "get_ds_product": self.dropshipping.get_ds_product,
            "get_ds_categories": self.dropshipping.get_ds_categories,
            "add_dropshipper": self.dropshipping.add_dropshipper,
            "get_ds_orders": self.dropshipping.get_ds_orders,
            "get_ds_trade_order": self.dropshipping.get_ds_trade_order,
            "get_ds_commission_orders": self.dropshipping.get_ds_commission_orders,
            "ds_image_search": self.dropshipping.ds_image_search,
            "get_ds_recommend_feed": self.dropshipping.get_ds_recommend_feed,
            "create_ds_order": self.dropshipping.create_ds_order,
            "query_ds_freight": self.dropshipping.query_ds_freight,
            "get_ds_order_tracking": self.dropshipping.get_ds_order_tracking,
            "get_ds_feed_items": self.dropshipping.get_ds_feed_items,
            "get_ds_product_special_info": self.dropshipping.get_ds_product_special_info,
            "get_ds_wholesale_product": self.dropshipping.get_ds_wholesale_product,
            "text_search_ds": self.dropshipping.text_search_ds,
            "report_ds_search_event": self.dropshipping.report_ds_search_event,
            "get_ds_member_benefit": self.dropshipping.get_ds_member_benefit,
            "get_trade_ds_order": self.dropshipping.get_trade_ds_order,
        }

        if name in method_map:
            return method_map[name]

        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{name}'"
        )
