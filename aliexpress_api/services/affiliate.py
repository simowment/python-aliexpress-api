"""Affiliate service for AliExpress API.

This module provides affiliate marketing methods for the AliExpress API.
"""

from typing import List, Union, Optional

from .base import BaseService
from .. import models
from ..sdk import api as aliapi
from ..helpers import api_request, get_list_as_string
from ..errors import (
    ProductsNotFoundException,
    InvalidTrackingIdException,
    OrdersNotFoundException,
)


class AffiliateService(BaseService):
    """Service providing affiliate marketing methods.

    Example:
        >>> from aliexpress_api import AliexpressApi
        >>> api = AliexpressApi(KEY, SECRET, tracking_id="YOUR_TRACKING_ID")
        >>> links = api.affiliate.get_affiliate_links("https://aliexpress.com/item/123.html")
    """

    def get_affiliate_links(
        self,
        links: Union[str, List[str]],
        link_type: models.LinkType = models.LinkType.NORMAL,
    ) -> List[models.AffiliateLink]:
        """Convert links to affiliate links.

        Args:
            links: One or more links to convert.
            link_type: Choose between normal link or hot link with higher commission.

        Returns:
            List of AffiliateLink objects containing promotion links.

        Raises:
            InvalidTrackingIdException: If tracking_id is not set.
            ApiRequestException: If the request fails.
        """
        if not self._tracking_id:
            raise InvalidTrackingIdException(
                "The tracking id is required for affiliate links"
            )

        links_str = get_list_as_string(links)

        request = self._prepare_request(
            aliapi.rest.AliexpressAffiliateLinkGenerateRequest(),
            source_values=links_str,
            promotion_link_type=link_type,
            tracking_id=self._tracking_id,
        )

        response = api_request(
            request,
            "aliexpress_affiliate_link_generate_response",
            models.AffiliateLink,
        )

        # generate-link returns a list of links
        if response and hasattr(response, "promotion_links"):
            return response.promotion_links

        return response

    def get_hotproducts(
        self,
        category_ids: Union[str, List[str]] = None,
        delivery_days: int = None,
        fields: Union[str, List[str]] = None,
        keywords: str = None,
        max_sale_price: int = None,
        min_sale_price: int = None,
        page_no: int = None,
        page_size: int = None,
        platform_product_type: models.ProductType = None,
        ship_to_country: str = None,
        sort: models.SortBy = None,
    ) -> models.HotProductsResponse:
        """Search for affiliated products with high commission.

        Args:
            category_ids: One or more category IDs.
            delivery_days: Estimated delivery days.
            fields: Fields to include in the results.
            keywords: Search products based on keywords.
            max_sale_price: Filter products below this price (in cents).
            min_sale_price: Filter products above this price (in cents).
            page_no: Page number.
            page_size: Products per page (1-50).
            platform_product_type: Specify platform product type.
            ship_to_country: Filter products available for this country.
            sort: Sort method.

        Returns:
            HotProductsResponse with products list.

        Raises:
            ProductsNotFoundException: If no products found.
            ApiRequestException: If the request fails.
        """
        request = self._prepare_request(
            aliapi.rest.AliexpressAffiliateHotproductQueryRequest(),
            category_ids=get_list_as_string(category_ids),
            delivery_days=str(delivery_days) if delivery_days else None,
            fields=get_list_as_string(fields),
            keywords=keywords,
            max_sale_price=max_sale_price,
            min_sale_price=min_sale_price,
            page_no=page_no,
            page_size=page_size,
            platform_product_type=platform_product_type,
            ship_to_country=ship_to_country,
            sort=sort,
            target_currency=self._currency,
            target_language=str(self._language).lower(),
            tracking_id=self._tracking_id,
        )

        response = api_request(
            request,
            "aliexpress_affiliate_hotproduct_query_response",
            models.HotProductsResponse,
        )

        if response and response.current_record_count > 0:
            return response
        else:
            raise ProductsNotFoundException("No products found with current parameters")

    def get_products(
        self,
        category_ids: Union[str, List[str]] = None,
        delivery_days: int = None,
        fields: Union[str, List[str]] = None,
        keywords: str = None,
        max_sale_price: int = None,
        min_sale_price: int = None,
        page_no: int = None,
        page_size: int = None,
        platform_product_type: models.ProductType = None,
        ship_to_country: str = None,
        sort: models.SortBy = None,
    ) -> models.ProductsResponse:
        """Search for affiliated products.

        Args:
            category_ids: One or more category IDs.
            delivery_days: Estimated delivery days.
            fields: Fields to include in the results.
            keywords: Search products based on keywords.
            max_sale_price: Filter products below this price (in cents).
            min_sale_price: Filter products above this price (in cents).
            page_no: Page number.
            page_size: Products per page (1-50).
            platform_product_type: Specify platform product type.
            ship_to_country: Filter products available for this country.
            sort: Sort method.

        Returns:
            ProductsResponse with products list.

        Raises:
            ProductsNotFoundException: If no products found.
            ApiRequestException: If the request fails.
        """
        request = self._prepare_request(
            aliapi.rest.AliexpressAffiliateProductQueryRequest(),
            category_ids=get_list_as_string(category_ids),
            delivery_days=str(delivery_days) if delivery_days else None,
            fields=get_list_as_string(fields),
            keywords=keywords,
            max_sale_price=max_sale_price,
            min_sale_price=min_sale_price,
            page_no=page_no,
            page_size=page_size,
            platform_product_type=platform_product_type,
            ship_to_country=ship_to_country,
            sort=sort,
            target_currency=self._currency,
            target_language=str(self._language).lower(),
            tracking_id=self._tracking_id,
        )

        response = api_request(
            request,
            "aliexpress_affiliate_product_query_response",
            models.ProductsResponse,
        )

        if response and response.current_record_count > 0:
            return response
        else:
            raise ProductsNotFoundException("No products found with current parameters")

    def smart_match_product(
        self,
        device_id: str,
        app: str = None,
        country: str = None,
        device: str = None,
        fields: Union[str, List[str]] = None,
        keywords: str = None,
        page_no: int = None,
        product_id: str = None,
        site: str = None,
        target_currency: str = None,
        target_language: str = None,
        tracking_id: str = None,
        user: str = None,
    ) -> models.HotProductsResponse:
        """Get affiliated products using smart match.

        Args:
            device_id: Unique device ID.
            app: Application identifier.
            country: Country code for targeting.
            device: Device type (e.g., "mobile", "desktop").
            fields: Fields to include in the results.
            keywords: Search keywords.
            page_no: Page number.
            product_id: Specific product ID to match.
            site: Site information.
            target_currency: Currency code for prices.
            target_language: Language code for results.
            tracking_id: Affiliate tracking ID.
            user: User identifier.

        Returns:
            HotProductsResponse with matched products.

        Raises:
            ProductsNotFoundException: If no products found.
            ApiRequestException: If the request fails.
        """
        request = self._prepare_request(
            aliapi.rest.AliexpressAffiliateProductSmartmatchRequest(),
            app=app,
            country=country,
            device=device,
            device_id=device_id,
            fields=get_list_as_string(fields),
            keywords=keywords,
            page_no=page_no,
            product_id=product_id,
            site=site,
            target_currency=target_currency or self._currency,
            target_language=target_language or str(self._language).lower(),
            tracking_id=tracking_id or self._tracking_id,
            user=user,
        )

        response = api_request(
            request,
            "aliexpress_affiliate_product_smartmatch_response",
            models.HotProductsResponse,
        )

        if response and response.current_record_count > 0:
            return response
        else:
            raise ProductsNotFoundException("No products found with current parameters")

    def get_order_list(
        self,
        status: str,
        start_time: str,
        end_time: str,
        fields: Union[str, List[str]] = None,
        locale_site: str = None,
        page_no: int = None,
        page_size: int = None,
    ) -> models.OrderListResponse:
        """Retrieve affiliate orders from AliExpress.

        Args:
            status: Order status filter (e.g., 'Payment Completed').
            start_time: Start time in format 'YYYY-MM-DD HH:MM:SS'.
            end_time: End time in format 'YYYY-MM-DD HH:MM:SS'.
            fields: Fields to include in results.
            locale_site: Locale site (e.g., 'ru_site').
            page_no: Page number.
            page_size: Records per page (up to 50).

        Returns:
            OrderListResponse with orders list.

        Raises:
            OrdersNotFoundException: If no orders found.
            ApiRequestException: If the request fails.
        """
        request = self._prepare_request(
            aliapi.rest.AliexpressAffiliateOrderListRequest(),
            start_time=start_time,
            end_time=end_time,
            fields=get_list_as_string(fields),
            locale_site=locale_site or self._get_locale(),
            page_no=page_no,
            page_size=page_size,
            status=status,
        )

        response = api_request(
            request,
            "aliexpress_affiliate_order_list_response",
            models.OrderListResponse,
        )

        if response and response.current_record_count > 0:
            return response
        else:
            raise OrdersNotFoundException(
                "No orders found for the specified parameters"
            )
