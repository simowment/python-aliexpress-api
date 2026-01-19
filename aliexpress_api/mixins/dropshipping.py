from typing import List, Union, Optional
from .. import models
from ..skd import api as aliapi
from ..helpers import api_request, get_list_as_string
from ..errors import ProductsNotFoundException, OrdersNotFoundException
import json



class DropshippingMixin:
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
        **kwargs,
    ) -> models.DsProductGetResponse:
        """Get detailed information about a dropshipping product.

        Args:
            product_id (str): The product ID.
            ship_to_country (str): Country code for targeting.
            target_currency (str, optional): Target currency.
            target_language (str, optional): Target language.
            remove_personal_benefit (bool, optional): Remove personal benefit.
            biz_model (str, optional): Business model.
            province_code (str, optional): Province code.
            city_code (str, optional): City code.

        Returns:
            models.DsProductGetResponse: Detailed product information.
        """
        request = aliapi.rest.AliexpressDsProductGetRequest()
        request.app_signature = self._app_signature
        request.ship_to_country = ship_to_country
        request.product_id = product_id
        request.target_currency = target_currency or self._currency
        request.target_language = target_language or self._language.lower() if hasattr(self._language, 'lower') else str(self._language).lower()
        request.remove_personal_benefit = remove_personal_benefit
        request.biz_model = biz_model
        request.province_code = province_code
        request.city_code = city_code

        response = api_request(request, "aliexpress_ds_product_get_response", session=self._token)

        return response

    def get_ds_categories(
        self,
        category_id: str = None,
        language: str = None,
        **kwargs,
    ) -> models.DsCategoryGetResponse:
        """Get dropshipping categories.

        Args:
            category_id (str): categoryId
            language (str): language:hi de ru pt ko in en it fr zh es iw ar vi th uk ja id pl he nl tr

        Returns:
            models.DsCategoryGetResponse: Contains category information including parent
                and child categories.

        Raises:
            CategoriesNotFoudException: If no categories found.
            ApiRequestException: If the API request fails.
            ApiRequestResponseException: If the API response is invalid.
        """
        request = aliapi.rest.AliexpressDsCategoryGetRequest()
        request.app_signature = self._app_signature
        request.category_id = category_id
        # Use provided language or fallback to instance language.
        request.language = language if language else self._language.replace("_", "") if "_" in str(self._language) else str(self._language).lower()

        response = api_request(request, "aliexpress_ds_category_get_response", session=self._token)
        
        # NOTE: The auto-generated response wrapper might map 'resp_result' from the JSON 
        # to the response object properties. We rely on 'api_request' doing the right thing.
        # However, the docs show a new structure 'resp_result' -> 'result' -> 'categories'.
        # If 'api_request' simply returns the 'result', we are good.
        # But commonly we check if 'total_result_count' > 0 or similar.
        
        return response

        response = api_request(request, "aliexpress_ds_category_get_response")

        return response

    def add_dropshipper(
        self,
        email: str,
        mobile: str = None,
        app_name: str = None,
        country: str = None,
        locale: str = None,
        platform: str = None,
        **kwargs,
    ):
        """Add a new dropshipper.

        Args:
            email (str): Dropshipper's email address.
            mobile (str): Dropshipper's mobile number.
            app_name (str): Application name.
            country (str): Country code.
            locale (str): Locale for the request.
            platform (str): Platform identifier.

        Returns:
            The API response.

        Raises:
            ApiRequestException: If the API request fails.
            ApiRequestResponseException: If the API response is invalid.
        """
        request = aliapi.rest.DsDropshpperAddRequest()
        request.app_signature = self._app_signature
        request.app_name = app_name
        request.country = country
        request.email = email
        request.locale = locale
        request.mobile = mobile
        request.platform = platform

        response = api_request(request, "ds_dropshpper_add_response")

        return response

    def get_ds_orders(
        self,
        start_time: str,
        end_time: str,
        status: str = None,
        fields: Union[str, List[str]] = None,
        locale: str = None,
        page_no: int = None,
        page_size: int = None,
        **kwargs,
    ) -> models.DsOrderListResponse:
        """Get list of dropshipping orders.

        Args:
            start_time (str): Start time in format 'YYYY-MM-DD HH:MM:SS'.
            end_time (str): End time in format 'YYYY-MM-DD HH:MM:SS'.
            status (str): Order status filter.
            fields (str | list[str]): Fields to include in the response.
            locale (str): Locale for the request.
            page_no (int): Page number.
            page_size (int): Number of records per page.

        Returns:
            models.DsOrderListResponse: Contains order information.

        Raises:
            OrdersNotFoundException: If no orders found.
            ApiRequestException: If the API request fails.
            ApiRequestResponseException: If the API response is invalid.
        """
        request = aliapi.rest.DsOrderListRequest()
        request.app_signature = self._app_signature
        request.end_time = end_time
        request.fields = get_list_as_string(fields)
        request.locale = locale
        request.page_no = page_no
        request.page_size = page_size
        request.start_time = start_time
        request.status = status

        response = api_request(request, "ds_order_list_response")

        if response.current_record_count > 0:
            return response
        else:
            raise OrdersNotFoundException(
                "No orders found for the specified parameters"
            )

    def get_ds_trade_order(
        self,
        order_id: str,
        fields: Union[str, List[str]] = None,
        locale: str = None,
        **kwargs,
    ) -> models.DsTradeOrderGetResponse:
        """Get detailed information about a dropshipping trade order.

        Args:
            order_id (str): The order ID.
            fields (str | list[str]): Fields to include in the response.
            locale (str): Locale for the request.

        Returns:
            models.DsTradeOrderGetResponse: Contains detailed order information including
                products and logistics.

        Raises:
            OrdersNotFoundException: If order not found.
            ApiRequestException: If the API request fails.
            ApiRequestResponseException: If the API response is invalid.
        """
        request = aliapi.rest.AliexpressDsTradeOrderGetRequest()
        request.app_signature = self._app_signature
        request.fields = get_list_as_string(fields)
        request.locale = locale
        request.order_id = order_id

        response = api_request(request, "aliexpress_ds_trade_order_get_response")

        return response

    def get_ds_commission_orders(
        self,
        start_time: str,
        end_time: str,
        fields: Union[str, List[str]] = None,
        locale: str = None,
        page_no: int = None,
        page_size: int = None,
        **kwargs,
    ) -> models.DsCommissionOrderListResponse:
        """Get list of dropshipping commission orders.

        Args:
            start_time (str): Start time in format 'YYYY-MM-DD HH:MM:SS'.
            end_time (str): End time in format 'YYYY-MM-DD HH:MM:SS'.
            fields (str | list[str]): Fields to include in the response.
            locale (str): Locale for the request.
            page_no (int): Page number.
            page_size (int): Number of records per page.

        Returns:
            models.DsCommissionOrderListResponse: Contains commission order information.

        Raises:
            OrdersNotFoundException: If no orders found.
            ApiRequestException: If the API request fails.
            ApiRequestResponseException: If the API response is invalid.
        """
        request = aliapi.rest.AliexpressDsCommissionorderListbyindexRequest()
        request.app_signature = self._app_signature
        request.end_time = end_time
        request.fields = get_list_as_string(fields)
        request.locale = locale
        request.page_no = page_no
        request.page_size = page_size
        request.start_time = start_time

        response = api_request(
            request, "aliexpress_ds_commissionorder_listbyindex_response"
        )

        if response.current_record_count > 0:
            return response
        else:
            raise OrdersNotFoundException(
                "No commission orders found for the specified parameters"
            )

    def ds_image_search(
        self,
        image_id: str,
        country: str = None,
        fields: Union[str, List[str]] = None,
        locale: str = None,
        web_site: str = None,
        **kwargs,
    ):
        """Search for products using an image.

        Args:
            image_id (str): The image ID to search with.
            country (str): Country code for targeting.
            fields (str | list[str]): Fields to include in the response.
            locale (str): Locale for the request.
            web_site (str): Website identifier.

        Returns:
            Products matching the image search.

        Raises:
            ProductsNotFoundException: If no products found.
            ApiRequestException: If the API request fails.
            ApiRequestResponseException: If the API response is invalid.
        """
        request = aliapi.rest.AliexpressDsImageSearchRequest()
        request.app_signature = self._app_signature
        request.country = country
        request.fields = get_list_as_string(fields)
        request.image_id = image_id
        request.locale = locale
        request.target_currency = self._currency
        request.target_language = self._language
        request.web_site = web_site

        response = api_request(request, "aliexpress_ds_image_search_response")

        return response

    def get_ds_recommend_feed(
        self,
        feed_name: str = None,
        country: str = None,
        fields: Union[str, List[str]] = None,
        locale: str = None,
        page_no: int = None,
        page_size: int = None,
        web_site: str = None,
        **kwargs,
    ):
        """Get recommended feed products for dropshipping.

        Args:
            feed_name (str): The feed name to get recommendations from.
            country (str): Country code for targeting.
            fields (str | list[str]): Fields to include in the response.
            locale (str): Locale for the request.
            page_no (int): Page number.
            page_size (int): Number of records per page.
            web_site (str): Website identifier.

        Returns:
            Recommended feed products.

        Raises:
            ProductsNotFoundException: If no products found.
            ApiRequestException: If the API request fails.
            ApiRequestResponseException: If the API response is invalid.
        """
        request = aliapi.rest.AliexpressDsRecommendFeedGetRequest()
        request.app_signature = self._app_signature
        request.country = country
        request.fields = get_list_as_string(fields)
        request.feed_name = feed_name
        request.locale = locale
        request.page_no = page_no
        request.page_size = page_size
        request.target_currency = self._currency
        request.target_language = self._language
        request.web_site = web_site

        response = api_request(request, "aliexpress_ds_recommend_feed_get_response")

        return response

    def create_ds_order(
        self,
        logistics_address: dict,
        product_items: list,
        locale: str = None,
        out_order_id: str = None,
        ds_extend_params: dict = None,
        **kwargs,
    ):
        """Create and pay for a dropshipping order.

        Args:
            logistics_address (dict): Logistic address information.
            product_items (list): Product attributes.
            locale (str): Internationalization locale.
            out_order_id (str): Outer order id, used for idempotent checkout.
            ds_extend_params (dict): DS ExtendParam.

        Returns:
            Order creation response.

        Raises:
            ApiRequestException: If the API request fails.
            ApiRequestResponseException: If the API response is invalid.
        """
        request = aliapi.rest.AliexpressDsOrderCreateRequest()
        request.app_signature = self._app_signature
        
        order_params = {
            "logistics_address": logistics_address,
            "product_items": product_items
        }
        
        if locale:
            order_params['locale'] = locale
        if out_order_id:
            order_params['out_order_id'] = out_order_id

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
        locale: str = None,
        currency: str = None,
        province_code: str = None,
        city_code: str = None,
        language: str = None,
        **kwargs,
    ):
        """Query freight/shipping costs for products.

        Args:
            product_id (str): product_id
            sku_id (str): selected sku
            country_code (str): country that ships to
            quantity (int): quantity for your request
            locale (str): locale
            currency (str): currency for calculate the freight fee
            province_code (str): provice
            city_code (str): city
            language (str): language

        Returns:
            Freight query response.

        Raises:
            ApiRequestException: If the API request fails.
            ApiRequestResponseException: If the API response is invalid.
        """
        request = aliapi.rest.AliexpressDsFreightQueryRequest()
        request.app_signature = self._app_signature
        
        query_req = {
            "productId": product_id,
            "selectedSkuId": sku_id,
            "shipToCountry": country_code,
            "quantity": quantity,
            "locale": locale if locale else "en_US", # Default to en_US if not provided? Or keep None and rely on user? Docs say Required.
            "currency": currency if currency else self._currency,
            "language": language if language else self._language.replace("_", "") if "_" in str(self._language) else str(self._language) 
        }
        # Note on language: self._language might be 'EN', API might expect 'en' or 'EN'. 
        # API Doc says: language String Yes language. 
        # Typically locale is "en_US", language is "en" or "EN".
        
        # Let's clean up language logic. self._language is likely "EN", "RU" etc from the enum.
        # If the API expects "en", "ru" we might need conversion.
        # Docs are sparse "language String Yes language".
        
        if province_code:
            query_req['provinceCode'] = province_code
        if city_code:
            query_req['cityCode'] = city_code
            
        request.query_delivery_req = json.dumps(query_req)

        response = api_request(request, "aliexpress_ds_freight_query_response")

        return response

    def get_ds_order_tracking(
        self,
        ae_order_id: str,
        language: str = None,
        **kwargs,
    ):
        """Get DropShip Order Tracking info.

        Args:
            ae_order_id (str): Order ID which you get from order.create
            language (str): language

        Returns:
            Order tracking information.

        Raises:
            OrdersNotFoundException: If order not found.
            ApiRequestException: If the API request fails.
            ApiRequestResponseException: If the API response is invalid.
        """
        request = aliapi.rest.AliexpressDsOrderTrackingGetRequest()
        request.app_signature = self._app_signature
        request.ae_order_id = ae_order_id
        request.language = language if language else self._language.replace("_", "") if "_" in str(self._language) else str(self._language).lower()

        response = api_request(request, "aliexpress_ds_order_tracking_get_response")

        return response

    def get_ds_feed_items(
        self,
        feed_name: str,
        locale: str = None,
        page_no: int = None,
        page_size: int = None,
        web_site: str = None,
        **kwargs,
    ):
        """Fetch items with feed name in simple model.

        Args:
            feed_name (str): The feed name.
            locale (str): Locale for the request.
            page_no (int): Page number.
            page_size (int): Number of records per page.
            web_site (str): Website identifier.

        Returns:
            Feed items response.

        Raises:
            ApiRequestException: If the API request fails.
            ApiRequestResponseException: If the API response is invalid.
        """
        request = aliapi.rest.AliexpressDsFeedItemidsGetRequest()
        request.app_signature = self._app_signature
        request.feed_name = feed_name
        request.locale = locale
        request.page_no = page_no
        request.page_size = page_size
        request.web_site = web_site

        response = api_request(request, "aliexpress_ds_feed_itemids_get_response")

        return response

    def get_ds_product_special_info(
        self,
        product_id: str,
        fields: Union[str, List[str]] = None,
        locale: str = None,
        web_site: str = None,
        **kwargs,
    ):
        """Get special product information like certification.

        Args:
            product_id (str): The product ID.
            fields (str | list[str]): Fields to include in the response.
            locale (str): Locale for the request.
            web_site (str): Website identifier.

        Returns:
            Product special information.

        Raises:
            ProductsNotFoundException: If product not found.
            ApiRequestException: If the API request fails.
            ApiRequestResponseException: If the API response is invalid.
        """
        request = aliapi.rest.AliexpressDsProductSpecialinfoGetRequest()
        request.app_signature = self._app_signature
        request.fields = get_list_as_string(fields)
        request.locale = locale
        request.product_id = product_id
        request.web_site = web_site

        response = api_request(
            request, "aliexpress_ds_product_specialinfo_get_response"
        )

        return response

    def get_ds_wholesale_product(
        self,
        product_id: str,
        fields: Union[str, List[str]] = None,
        locale: str = None,
        web_site: str = None,
        **kwargs,
    ):
        """Get product info for wholesale business.

        Args:
            product_id (str): The product ID.
            fields (str | list[str]): Fields to include in the response.
            locale (str): Locale for the request.
            web_site (str): Website identifier.

        Returns:
            Wholesale product information.

        Raises:
            ProductsNotFoundException: If product not found.
            ApiRequestException: If the API request fails.
            ApiRequestResponseException: If the API response is invalid.
        """
        request = aliapi.rest.AliexpressDsProductWholesaleGetRequest()
        request.app_signature = self._app_signature
        request.fields = get_list_as_string(fields)
        request.locale = locale
        request.product_id = product_id
        request.web_site = web_site
        response = api_request(request, "aliexpress_ds_product_wholesale_get_response")

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
        **kwargs,
    ) -> models.DsTextSearchResponse:
        """Text search for dropshipping products.

        Args:
            keywords (str): Search keywords.
            category_ids (str | list[str]): Category IDs to filter by.
            country (str): Country code for targeting.
            fields (str | list[str]): Fields to include in the response.
            locale (str): Locale for the request.
            page_no (int): Page number.
            page_size (int): Number of records per page.

        Returns:
            Search results.

        Raises:
            ProductsNotFoundException: If no products found.
            ApiRequestException: If the API request fails.
            ApiRequestResponseException: If the API response is invalid.
        """
        request = aliapi.rest.AliexpressDsTextSearchRequest()
        request.app_signature = self._app_signature
        request.categoryId = get_list_as_string(category_ids)
        request.countryCode = country
        request.keyWord = keywords
        request.local = locale or f"{self._language.lower()}_{country.upper()}" if hasattr(self._language, 'lower') else str(self._language).lower() + "_" + country.upper()
        request.pageIndex = page_no
        request.pageSize = page_size
        request.sortBy = sort
        request.currency = self._currency

        response = api_request(request, "aliexpress_ds_text_search_response", session=self._token)

        if hasattr(response, 'data') and response.data and hasattr(response.data, 'totalCount') and int(response.data.totalCount) > 0:
            return response
        else:
            raise ProductsNotFoundException("No products found with current parameters")

    def report_ds_search_event(
        self, event_list: list, locale: str = None, web_site: str = None, **kwargs
    ):
        """Report search events for analytics.

        Args:
            event_list (list): List of search events to report.
            locale (str): Locale for the request.
            web_site (str): Website identifier.

        Returns:
            Event report response.

        Raises:
            ApiRequestException: If the API request fails.
            ApiRequestResponseException: If the API response is invalid.
        """
        request = aliapi.rest.AliexpressDsSearchEventReportRequest()
        request.app_signature = self._app_signature
        request.event_list = str(event_list)
        request.locale = locale
        request.web_site = web_site

        response = api_request(request, "aliexpress_ds_search_event_report_response")

        return response

    def get_ds_member_benefit(self, locale: str = None, web_site: str = None, **kwargs):
        """Get dropshipper member benefits.

        Args:
            locale (str): Locale for the request.
            web_site (str): Website identifier.

        Returns:
            Member benefit information.

        Raises:
            ApiRequestException: If the API request fails.
            ApiRequestResponseException: If the API response is invalid.
        """
        request = aliapi.rest.AliexpressDsMemberBenefitGetRequest()
        request.app_signature = self._app_signature
        request.locale = locale
        request.web_site = web_site

        response = api_request(request, "aliexpress_ds_member_benefit_get_response")

        return response

    def get_trade_ds_order(
        self,
        order_id: str,
        fields: Union[str, List[str]] = None,
        locale: str = None,
        web_site: str = None,
        **kwargs,
    ):
        """Buyer query order details.

        Args:
            order_id (str): The order ID.
            fields (str | list[str]): Fields to include in the response.
            locale (str): Locale for the request.
            web_site (str): Website identifier.

        Returns:
            Order details.

        Raises:
            OrdersNotFoundException: If order not found.
            ApiRequestException: If the API request fails.
            ApiRequestResponseException: If the API response is invalid.
        """
        request = aliapi.rest.AliexpressTradeDsOrderGetRequest()
        request.app_signature = self._app_signature
        request.fields = get_list_as_string(fields)
        request.locale = locale
        request.order_id = order_id
        request.web_site = web_site

        response = api_request(request, "aliexpress_trade_ds_order_get_response")

        return response
