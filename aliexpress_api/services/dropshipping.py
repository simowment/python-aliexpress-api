"""Dropshipping service for AliExpress API.

This module provides dropshipping-specific methods for the AliExpress API.
"""

import json
from typing import List, Union, Optional

from .base import BaseService
from .. import models
from ..sdk import api as aliapi
from ..helpers import api_request, get_list_as_string
from ..errors import ProductsNotFoundException, OrdersNotFoundException


class DropshippingService(BaseService):
    """Service providing dropshipping methods.

    Example:
        >>> from aliexpress_api import AliexpressApi
        >>> api = AliexpressApi(KEY, SECRET, token="YOUR_TOKEN")
        >>> product = api.dropshipping.get_ds_product("1005001234567890", "US")
    """

    def get_ds_product(
        self,
        product_id: str,
        ship_to_country: str,
        target_currency: Optional[str] = None,
        target_language: Optional[str] = None,
        remove_personal_benefit: Optional[bool] = None,
        biz_model: Optional[str] = None,
        province_code: Optional[str] = None,
        city_code: Optional[str] = None,
        locale: Optional[str] = None,
    ) -> models.DsProductGetResponse:
        """Get detailed information about a dropshipping product.

        Args:
            product_id: The product ID.
            ship_to_country: Country code for targeting.
            target_currency: Target currency.
            target_language: Target language.
            remove_personal_benefit: Remove personal benefit.
            biz_model: Business model.
            province_code: Province code.
            city_code: City code.
            locale: Locale for the request.

        Returns:
            DsProductGetResponse with detailed product information.
        """
        request = self._prepare_request(
            aliapi.rest.AliexpressDsProductGetRequest(),
            product_id=product_id,
            ship_to_country=ship_to_country,
            target_currency=target_currency or self._currency,
            target_language=target_language or str(self._language).lower(),
            remove_personal_benefit=remove_personal_benefit,
            biz_model=biz_model,
            province_code=province_code,
            city_code=city_code,
            locale=locale or self._get_locale(ship_to_country),
        )

        response = api_request(
            request,
            "aliexpress_ds_product_get_response",
            models.DsProductGetResponse,
            session=self._token,
        )

        return response

    def get_ds_categories(
        self,
        category_id: Optional[str] = None,
        language: Optional[str] = None,
    ) -> models.DsCategoryGetResponse:
        """Get dropshipping categories.

        Args:
            category_id: Category ID.
            language: Language for results.

        Returns:
            DsCategoryGetResponse with category information.
        """
        request = self._prepare_request(
            aliapi.rest.AliexpressDsCategoryGetRequest(),
            category_id=category_id,
            language=language or str(self._language).lower(),
        )

        response = api_request(
            request,
            "aliexpress_ds_category_get_response",
            models.DsCategoryGetResponse,
            session=self._token,
        )

        return response

    def add_dropshipper(
        self,
        email: str,
        mobile: Optional[str] = None,
        app_name: Optional[str] = None,
        country: Optional[str] = None,
        locale: Optional[str] = None,
        platform: Optional[str] = None,
    ):
        """Add a new dropshipper.

        Args:
            email: Dropshipper's email address.
            mobile: Dropshipper's mobile number.
            app_name: Application name.
            country: Country code.
            locale: Locale for the request.
            platform: Platform identifier.

        Returns:
            API response.
        """
        request = self._prepare_request(
            aliapi.rest.DsDropshpperAddRequest(),
            app_name=app_name,
            country=country,
            email=email,
            locale=locale,
            mobile=mobile,
            platform=platform,
        )

        response = api_request(request, "ds_dropshpper_add_response")

        return response

    def get_ds_orders(
        self,
        start_time: str,
        end_time: str,
        status: Optional[str] = None,
        fields: Union[str, List[str]] = None,
        locale: Optional[str] = None,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> models.DsOrderListResponse:
        """Get list of dropshipping orders.

        Args:
            start_time: Start time in format 'YYYY-MM-DD HH:MM:SS'.
            end_time: End time in format 'YYYY-MM-DD HH:MM:SS'.
            status: Order status filter.
            fields: Fields to include in results.
            locale: Locale for the request.
            page_no: Page number.
            page_size: Records per page.

        Returns:
            DsOrderListResponse with order information.

        Raises:
            OrdersNotFoundException: If no orders found.
        """
        request = self._prepare_request(
            aliapi.rest.DsOrderListRequest(),
            end_time=end_time,
            fields=get_list_as_string(fields),
            locale=locale or self._get_locale(),
            page_no=page_no,
            page_size=page_size,
            start_time=start_time,
            status=status,
        )

        response = api_request(
            request,
            "ds_order_list_response",
            models.DsOrderListResponse,
        )

        if response and response.current_record_count > 0:
            return response
        else:
            raise OrdersNotFoundException(
                "No orders found for the specified parameters"
            )

    def get_ds_trade_order(
        self,
        order_id: str,
        fields: Union[str, List[str]] = None,
        locale: Optional[str] = None,
    ) -> models.DsTradeOrderGetResponse:
        """Get detailed dropshipping trade order information.

        Args:
            order_id: The order ID.
            fields: Fields to include in results.
            locale: Locale for the request.

        Returns:
            DsTradeOrderGetResponse with detailed order information.
        """
        request = self._prepare_request(
            aliapi.rest.AliexpressDsTradeOrderGetRequest(),
            fields=get_list_as_string(fields),
            locale=locale or self._get_locale(),
            order_id=order_id,
        )

        response = api_request(
            request,
            "aliexpress_ds_trade_order_get_response",
            models.DsTradeOrderGetResponse,
        )

        return response

    def get_ds_commission_orders(
        self,
        start_time: str,
        end_time: str,
        fields: Union[str, List[str]] = None,
        locale: Optional[str] = None,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> models.DsCommissionOrderListResponse:
        """Get dropshipping commission orders.

        Args:
            start_time: Start time in format 'YYYY-MM-DD HH:MM:SS'.
            end_time: End time in format 'YYYY-MM-DD HH:MM:SS'.
            fields: Fields to include in results.
            locale: Locale for the request.
            page_no: Page number.
            page_size: Records per page.

        Returns:
            DsCommissionOrderListResponse with commission orders.

        Raises:
            OrdersNotFoundException: If no commission orders found.
        """
        request = self._prepare_request(
            aliapi.rest.AliexpressDsCommissionorderListbyindexRequest(),
            end_time=end_time,
            fields=get_list_as_string(fields),
            locale=locale or self._get_locale(),
            page_no=page_no,
            page_size=page_size,
            start_time=start_time,
        )

        response = api_request(
            request,
            "aliexpress_ds_commissionorder_listbyindex_response",
            models.DsCommissionOrderListResponse,
        )

        if response and response.current_record_count > 0:
            return response
        else:
            raise OrdersNotFoundException(
                "No commission orders found for the specified parameters"
            )

    def ds_image_search(
        self,
        image_bytes: bytes,
        sort: str = "default",
        search_type: int = 0,
        limit: int = 20,
        target_currency: Optional[str] = None,
        target_language: Optional[str] = None,
    ):
        """Search products using an image (V2).

        Args:
            image_bytes: The image file bytes.
            sort: Sort method (default, min_price, max_price, sales, last_volume).
            search_type: 0 for image search, 1 for similar product search.
            limit: Number of results (1-50).
            target_currency: Target currency.
            target_language: Target language.

        Returns:
            Products matching the image search.
        """
        request = self._prepare_request(
            aliapi.rest.AliexpressDsImageSearchV2Request(),
            image_file_bytes=image_bytes,
            sort=sort,
            search_type=search_type,
            limit=limit,
            target_currency=target_currency or self._currency,
            target_language=target_language or str(self._language).lower(),
        )

        response = api_request(
            request,
            "aliexpress_ds_image_search_v2_response",
            session=self._token,
        )

        return response

    def get_ds_recommend_feed(
        self,
        feed_name: Optional[str] = None,
        country: Optional[str] = None,
        fields: Union[str, List[str]] = None,
        locale: Optional[str] = None,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
        web_site: Optional[str] = None,
    ):
        """Get recommended feed products for dropshipping.

        Args:
            feed_name: The feed name to get recommendations from.
            country: Country code for targeting.
            fields: Fields to include in results.
            locale: Locale for the request.
            page_no: Page number.
            page_size: Records per page.
            web_site: Website identifier.

        Returns:
            Recommended feed products.
        """
        request = self._prepare_request(
            aliapi.rest.AliexpressDsRecommendFeedGetRequest(),
            country=country,
            fields=get_list_as_string(fields),
            feed_name=feed_name,
            locale=locale or self._get_locale(country),
            page_no=page_no,
            page_size=page_size,
            target_currency=self._currency,
            target_language=str(self._language).lower(),
            web_site=web_site,
        )

        response = api_request(request, "aliexpress_ds_recommend_feed_get_response")

        return response

    def create_ds_order(
        self,
        logistics_address: dict,
        product_items: list,
        locale: Optional[str] = None,
        out_order_id: Optional[str] = None,
        ds_extend_params: Optional[dict] = None,
    ):
        """Create and pay for a dropshipping order.

        Args:
            logistics_address: Logistic address information.
            product_items: Product attributes.
            locale: Internationalization locale.
            out_order_id: Outer order id for idempotent checkout.
            ds_extend_params: DS ExtendParam.

        Returns:
            Order creation response.
        """
        request = self._prepare_request(
            aliapi.rest.AliexpressDsOrderCreateRequest(),
        )

        # Ensure locale is included in logistics_address
        logistics_address_with_locale = logistics_address.copy()
        if "locale" not in logistics_address_with_locale:
            logistics_address_with_locale["locale"] = locale or self._get_locale()

        order_params = {
            "logistics_address": logistics_address_with_locale,
            "product_items": product_items,
        }

        if out_order_id:
            order_params["out_order_id"] = out_order_id

        request.param_place_order_request4_open_api_d_t_o = json.dumps(order_params)

        if ds_extend_params:
            request.ds_extend_request = json.dumps(ds_extend_params)

        response = api_request(request, "aliexpress_ds_order_create_response")

        return response

    def query_ds_freight(
        self,
        product_id: str,
        sku_id: str,
        country_code: str,
        quantity: int,
        locale: Optional[str] = None,
        currency: Optional[str] = None,
        province_code: Optional[str] = None,
        city_code: Optional[str] = None,
        language: Optional[str] = None,
    ):
        """Query freight/shipping costs for products.

        Args:
            product_id: Product ID.
            sku_id: Selected SKU.
            country_code: Country that ships to.
            quantity: Quantity for the request.
            locale: Locale for the request.
            currency: Currency for freight fee calculation.
            province_code: Province code.
            city_code: City code.
            language: Language for the request.

        Returns:
            Freight query response.
        """
        request = self._prepare_request(
            aliapi.rest.AliexpressDsFreightQueryRequest(),
        )

        query_req = {
            "productId": product_id,
            "selectedSkuId": sku_id,
            "shipToCountry": country_code,
            "quantity": quantity,
            "locale": locale or self._get_locale(country_code),
            "currency": currency or self._currency,
            "language": language or str(self._language).lower(),
        }

        if province_code:
            query_req["provinceCode"] = province_code
        if city_code:
            query_req["cityCode"] = city_code

        request.query_delivery_req = json.dumps(query_req)

        response = api_request(request, "aliexpress_ds_freight_query_response")

        return response

    def get_ds_order_tracking(
        self,
        ae_order_id: str,
        language: Optional[str] = None,
    ) -> models.DsOrderTrackingGetResponse:
        """Get dropshipping order tracking information.

        Args:
            ae_order_id: Order ID from order creation.
            language: Language for the request.

        Returns:
            DsOrderTrackingGetResponse with tracking information.
        """
        request = self._prepare_request(
            aliapi.rest.AliexpressDsOrderTrackingGetRequest(),
            ae_order_id=ae_order_id,
            language=language or str(self._language).lower(),
        )

        response = api_request(
            request,
            "aliexpress_ds_order_tracking_get_response",
            models.DsOrderTrackingGetResponse,
            session=self._token,
        )

        return response

    def get_ds_feed_items(
        self,
        feed_name: str,
        locale: Optional[str] = None,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
        web_site: Optional[str] = None,
    ):
        """Fetch items with feed name.

        Args:
            feed_name: The feed name.
            locale: Locale for the request.
            page_no: Page number.
            page_size: Records per page.
            web_site: Website identifier.

        Returns:
            Feed items response.
        """
        request = self._prepare_request(
            aliapi.rest.AliexpressDsFeedItemidsGetRequest(),
            feed_name=feed_name,
            locale=locale or self._get_locale(),
            page_no=page_no,
            page_size=page_size,
            web_site=web_site,
        )

        response = api_request(
            request,
            "aliexpress_ds_feed_itemids_get_response",
            models.DsFeedItemIdsGetResponse,
            session=self._token,
        )

        return response

    def get_ds_product_special_info(
        self,
        product_id: str,
        fields: Union[str, List[str]] = None,
        locale: Optional[str] = None,
        web_site: Optional[str] = None,
    ):
        """Get special product information like certification.

        Args:
            product_id: The product ID.
            fields: Fields to include in results.
            locale: Locale for the request.
            web_site: Website identifier.

        Returns:
            Product special information.
        """
        request = self._prepare_request(
            aliapi.rest.AliexpressDsProductSpecialinfoGetRequest(),
            fields=get_list_as_string(fields),
            locale=locale or self._get_locale(),
            product_id=product_id,
            web_site=web_site,
        )

        response = api_request(
            request,
            "aliexpress_ds_product_specialinfo_get_response",
            models.DsProductSpecialInfoGetResponse,
            session=self._token,
        )

        return response

    def get_ds_wholesale_product(
        self,
        product_id: str,
        fields: Union[str, List[str]] = None,
        locale: Optional[str] = None,
        web_site: Optional[str] = None,
    ):
        """Get product info for wholesale business.

        Args:
            product_id: The product ID.
            fields: Fields to include in results.
            locale: Locale for the request.
            web_site: Website identifier.

        Returns:
            Wholesale product information.
        """
        request = self._prepare_request(
            aliapi.rest.AliexpressDsProductWholesaleGetRequest(),
            fields=get_list_as_string(fields),
            locale=locale or self._get_locale(),
            product_id=product_id,
            web_site=web_site,
        )

        response = api_request(
            request,
            "aliexpress_ds_product_wholesale_get_response",
            models.DsProductWholesaleGetResponse,
            session=self._token,
        )

        return response

    def text_search_ds(
        self,
        keywords: str,
        country: str,
        category_ids: Optional[Union[str, List[str]]] = None,
        locale: Optional[str] = None,
        sort: Optional[str] = None,
        page_no: Optional[int] = None,
        page_size: Optional[int] = None,
        min_price: Optional[str] = None,
        max_price: Optional[str] = None,
    ) -> models.DsTextSearchResponse:
        """Text search for dropshipping products.

        Args:
            keywords: Search keywords.
            category_ids: Category IDs to filter by.
            country: Country code for targeting.
            locale: Locale for the request.
            sort: Sort method.
            page_no: Page number.
            page_size: Records per page.
            min_price: Minimum price filter.
            max_price: Maximum price filter.

        Returns:
            DsTextSearchResponse with search results.

        Raises:
            ProductsNotFoundException: If no products found.
        """
        request = self._prepare_request(
            aliapi.rest.AliexpressDsTextSearchRequest(),
            categoryId=get_list_as_string(category_ids),
            countryCode=country,
            keyWord=keywords,
            local=locale or self._get_locale(country),
            pageIndex=page_no,
            pageSize=page_size,
            sortBy=sort,
            currency=self._currency,
        )

        response = api_request(
            request,
            "aliexpress_ds_text_search_response",
            models.DsTextSearchResponse,
            session=self._token,
        )

        if response and response.data and response.data.totalCount > 0:
            return response
        else:
            raise ProductsNotFoundException("No products found with current parameters")

    def report_ds_search_event(
        self,
        event_list: list,
        locale: Optional[str] = None,
        web_site: Optional[str] = None,
    ):
        """Report search events for analytics.

        Args:
            event_list: List of search events to report.
            locale: Locale for the request.
            web_site: Website identifier.

        Returns:
            Event report response.
        """
        request = self._prepare_request(
            aliapi.rest.AliexpressDsSearchEventReportRequest(),
            event_list=str(event_list),
            locale=locale or self._get_locale(),
            web_site=web_site,
        )

        response = api_request(
            request,
            "aliexpress_ds_search_event_report_response",
            models.DsSearchEventReportResponse,
            session=self._token,
        )

        return response

    def get_ds_member_benefit(
        self,
        locale: Optional[str] = None,
        web_site: Optional[str] = None,
    ):
        """Get dropshipper member benefits.

        Args:
            locale: Locale for the request.
            web_site: Website identifier.

        Returns:
            Member benefit information.
        """
        request = self._prepare_request(
            aliapi.rest.AliexpressDsMemberBenefitGetRequest(),
            locale=locale or self._get_locale(),
            web_site=web_site,
        )

        response = api_request(
            request,
            "aliexpress_ds_member_benefit_get_response",
            models.DsMemberBenefitGetResponse,
            session=self._token,
        )

        return response

    def get_trade_ds_order(
        self,
        order_id: str,
        fields: Union[str, List[str]] = None,
        locale: Optional[str] = None,
        web_site: Optional[str] = None,
    ):
        """Buyer query order details.

        Args:
            order_id: The order ID.
            fields: Fields to include in results.
            locale: Locale for the request.
            web_site: Website identifier.

        Returns:
            Order details.
        """
        request = self._prepare_request(
            aliapi.rest.AliexpressTradeDsOrderGetRequest(),
            fields=get_list_as_string(fields),
            locale=locale or self._get_locale(),
            order_id=order_id,
            web_site=web_site,
        )

        response = api_request(
            request,
            "aliexpress_trade_ds_order_get_response",
            models.DsTradeOrderGetResponse,
        )

        return response
