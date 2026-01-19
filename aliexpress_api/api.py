"""AliExpress API wrapper for Python

A simple Python wrapper for the AliExpress Open Platform API. This module allows
to get product information and affiliate links from AliExpress using the official
API in an easier way.
"""

from aliexpress_api.errors.exceptions import CategoriesNotFoudException
from aliexpress_api.helpers.categories import filter_child_categories, filter_parent_categories
from aliexpress_api.models.category import ChildCategory
from .skd import setDefaultAppInfo
from .skd import api as aliapi
from .errors import ProductsNotFoudException, InvalidTrackingIdException, OrdersNotFoundException
from .helpers import api_request, parse_products, get_list_as_string, get_product_ids
from . import models

from typing import List, Union


class AliexpressApi:
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
        language: models.Language,
        currency: models.Currency,
        tracking_id: str = None,
        app_signature: str = None,
        **kwargs):
        self._key = key
        self._secret = secret
        self._tracking_id = tracking_id
        self._language = language
        self._currency = currency
        self._app_signature = app_signature
        self.categories = None
        setDefaultAppInfo(self._key, self._secret)


    def get_products_details(self,
        product_ids: Union[str, List[str]],
        fields: Union[str, List[str]] = None,
        country: str = None,
        **kwargs) -> List[models.Product]:
        """Get products information.

        Args:
            product_ids (``str | list[str]``): One or more links or product IDs.
            fields (``str | list[str]``): The fields to include in the results. Defaults to all.
            country (``str``): Filter products that can be sent to that country. Returns the price
                according to the country's tax rate policy.

        Returns:
            ``list[models.Product]``: A list of products.

        Raises:
            ``ProductsNotFoudException``
            ``InvalidArgumentException``
            ``ApiRequestException``
            ``ApiRequestResponseException``
        """
        product_ids = get_product_ids(product_ids)
        product_ids = get_list_as_string(product_ids)

        request = aliapi.rest.AliexpressAffiliateProductdetailGetRequest()
        request.app_signature = self._app_signature
        request.fields = get_list_as_string(fields)
        request.product_ids = product_ids
        request.country = country
        request.target_currency = self._currency
        request.target_language = self._language
        request.tracking_id = self._tracking_id

        response = api_request(request, 'aliexpress_affiliate_productdetail_get_response')

        if response.current_record_count > 0:
            response = parse_products(response.products.product)
            return response
        else:
            raise ProductsNotFoudException('No products found with current parameters')


    def get_affiliate_links(self,
        links: Union[str, List[str]],
        link_type: models.LinkType = models.LinkType.NORMAL,
        **kwargs) -> List[models.AffiliateLink]:
        """Converts a list of links in affiliate links.

        Args:
            links (``str | list[str]``): One or more links to convert.
            link_type (``models.LinkType``): Choose between normal link with standard commission
                or hot link with hot product commission. Defaults to NORMAL.

        Returns:
            ``list[models.AffiliateLink]``: A list containing the affiliate links.

        Raises:
            ``InvalidArgumentException``
            ``InvalidTrackingIdException``
            ``ProductsNotFoudException``
            ``ApiRequestException``
            ``ApiRequestResponseException``
        """
        if not self._tracking_id:
            raise InvalidTrackingIdException('The tracking id is required for affiliate links')

        links = get_list_as_string(links)

        request = aliapi.rest.AliexpressAffiliateLinkGenerateRequest()
        request.app_signature = self._app_signature
        request.source_values = links
        request.promotion_link_type = link_type
        request.tracking_id = self._tracking_id

        response = api_request(request, 'aliexpress_affiliate_link_generate_response')

        if response.total_result_count > 0:
            return response.promotion_links.promotion_link
        else:
            raise ProductsNotFoudException('Affiliate links not available')


    def get_hotproducts(self,
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
        **kwargs) -> models.HotProductsResponse:
        """Search for affiliated products with high commission.

        Args:
            category_ids (``str | list[str]``): One or more category IDs.
            delivery_days (``int``): Estimated delivery days.
            fields (``str | list[str]``): The fields to include in the results list. Defaults to all.
            keywords (``str``): Search products based on keywords.
            max_sale_price (``int``): Filters products with price below the specified value.
                Prices appear in lowest currency denomination. So $31.41 should be 3141.
            min_sale_price (``int``): Filters products with price above the specified value.
                Prices appear in lowest currency denomination. So $31.41 should be 3141.
            page_no (``int``):
            page_size (``int``): Products on each page. Should be between 1 and 50.
            platform_product_type (``models.ProductType``): Specify platform product type.
            ship_to_country (``str``): Filter products that can be sent to that country.
                Returns the price according to the country's tax rate policy.
            sort (``models.SortBy``): Specifies the sort method.

        Returns:
            ``models.HotProductsResponse``: Contains response information and the list of products.

        Raises:
            ``ProductsNotFoudException``
            ``ApiRequestException``
            ``ApiRequestResponseException``
        """
        request = aliapi.rest.AliexpressAffiliateHotproductQueryRequest()
        request.app_signature = self._app_signature
        request.category_ids = get_list_as_string(category_ids)
        request.delivery_days = str(delivery_days)
        request.fields = get_list_as_string(fields)
        request.keywords = keywords
        request.max_sale_price = max_sale_price
        request.min_sale_price = min_sale_price
        request.page_no = page_no
        request.page_size = page_size
        request.platform_product_type = platform_product_type
        request.ship_to_country = ship_to_country
        request.sort = sort
        request.target_currency = self._currency
        request.target_language = self._language
        request.tracking_id = self._tracking_id

        response = api_request(request, 'aliexpress_affiliate_hotproduct_query_response')

        if response.current_record_count > 0:
            response.products = parse_products(response.products.product)
            return response
        else:
            raise ProductsNotFoudException('No products found with current parameters')


    def get_products(self,
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
        **kwargs) -> models.ProductsResponse:
        """Search for affiliated products.

        Args:
            category_ids (``str | list[str]``): One or more category IDs.
            delivery_days (``int``): Estimated delivery days.
            fields (``str | list[str]``): The fields to include in the results list. Defaults to all.
            keywords (``str``): Search products based on keywords.
            max_sale_price (``int``): Filters products with price below the specified value.
                Prices appear in lowest currency denomination. So $31.41 should be 3141.
            min_sale_price (``int``): Filters products with price above the specified value.
                Prices appear in lowest currency denomination. So $31.41 should be 3141.
            page_no (``int``):
            page_size (``int``): Products on each page. Should be between 1 and 50.
            platform_product_type (``models.ProductType``): Specify platform product type.
            ship_to_country (``str``): Filter products that can be sent to that country.
                Returns the price according to the country's tax rate policy.
            sort (``models.SortBy``): Specifies the sort method.

        Returns:
            ``models.ProductsResponse``: Contains response information and the list of products.

        Raises:
            ``ProductsNotFoudException``
            ``ApiRequestException``
            ``ApiRequestResponseException``
        """
        request = aliapi.rest.AliexpressAffiliateProductQueryRequest()
        request.app_signature = self._app_signature
        request.category_ids = get_list_as_string(category_ids)
        request.delivery_days = str(delivery_days)
        request.fields = get_list_as_string(fields)
        request.keywords = keywords
        request.max_sale_price = max_sale_price
        request.min_sale_price = min_sale_price
        request.page_no = page_no
        request.page_size = page_size
        request.platform_product_type = platform_product_type
        request.ship_to_country = ship_to_country
        request.sort = sort
        request.target_currency = self._currency
        request.target_language = self._language
        request.tracking_id = self._tracking_id

        response = api_request(request, 'aliexpress_affiliate_product_query_response')

        if response.current_record_count > 0:
            response.products = parse_products(response.products.product)
            return response
        else:
            raise ProductsNotFoudException('No products found with current parameters')


    def get_categories(self, **kwargs) -> List[Union[models.Category, ChildCategory]]:
        """Get all available categories, both parent and child.

        Returns:
            ``list[models.Category | models.ChildCategory]``: A list of categories.

        Raises:
            ``CategoriesNotFoudException``
            ``ApiRequestException``
            ``ApiRequestResponseException``
        """
        request = aliapi.rest.AliexpressAffiliateCategoryGetRequest()
        request.app_signature = self._app_signature

        response = api_request(request, 'aliexpress_affiliate_category_get_response')

        if response.total_result_count > 0:
            self.categories = response.categories.category
            return self.categories
        else:
            raise CategoriesNotFoudException('No categories found')


    def get_parent_categories(self, use_cache=True, **kwargs) -> List[models.Category]:
        """Get all available parent categories.

        Args:
            use_cache (``bool``): Uses cached categories to reduce API requests.

        Returns:
            ``list[models.Category]``: A list of parent categories.

        Raises:
            ``CategoriesNotFoudException``
            ``ApiRequestException``
            ``ApiRequestResponseException``
        """
        if not use_cache or not self.categories:
            self.get_categories()
        return filter_parent_categories(self.categories)


    def get_child_categories(self, parent_category_id: int, use_cache=True, **kwargs) -> List[models.ChildCategory]:
        """Get all available child categories for a specific parent category.

        Args:
            parent_category_id (``int``): The parent category id.
            use_cache (``bool``): Uses cached categories to reduce API requests.

        Returns:
            ``list[models.ChildCategory]``: A list of child categories.

        Raises:
            ``CategoriesNotFoudException``
            ``ApiRequestException``
            ``ApiRequestResponseException``
        """
        if not use_cache or not self.categories:
            self.get_categories()
        return filter_child_categories(self.categories, parent_category_id)


    def smart_match_product(self,
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
            **kwargs) -> models.HotProductsResponse:
        """
        Get affiliated products using smart match based on keyword and device information.

        Args:
            country (``str``): Country code for target location.
            device (``str``): Device type for targeting (e.g., "mobile", "desktop").
            device_id (``str``): Unique device ID.
            fields (``str | list[str]``): Fields to include in the results list. Defaults to all.
            keywords (``str``): Search products based on keywords.
            page_no (``int``): Page number of results to fetch.
            product_id (``str``): Specific product ID to match (optional).
            site (``str``): Site information for product targeting.
            target_currency (``str``): Currency code for prices (default is EUR).
            target_language (``str``): Language code for results (default is ES).
            tracking_id (``str``): Affiliate tracking ID for results.
            user (``str``): User identifier for additional targeting (optional).

        Returns:
            ``models.ProductSmartmatchResponse``: Contains response information and the list of products.

        Raises:
            ``ProductsNotFoundException``
            ``ApiRequestException``
            ``ApiRequestResponseException``
        """
        request = aliapi.rest.AliexpressAffiliateProductSmartmatchRequest()
        request.app = app,
        request.app_signature = self._app_signature
        request.country = country
        request.device = device
        request.device_id = device_id
        request.fields = get_list_as_string(fields)
        request.keywords = keywords
        request.page_no = page_no
        request.product_id = product_id
        request.site = site
        request.target_currency = target_currency
        request.target_language = target_language
        request.tracking_id = tracking_id
        request.user = user

        response = api_request(request, 'aliexpress_affiliate_product_smartmatch_response')

        if hasattr(response, 'products') and response.products:
            response.products = parse_products(response.products.product)
            return response
        else:
            raise ProductsNotFoudException('No products found with current parameters')
        
    def get_order_list(self,
                       status: str,
                       start_time: str,
                       end_time: str,
                       fields: Union[str, List[str]] = None,
                       locale_site: str = None,
                       page_no: int = None,
                       page_size: int = None,
                       **kwargs) -> models.OrderListResponse:
        """
        Retrieve a list of affiliate orders from AliExpress.

        Args:
            start_time (str): Start time in format 'YYYY-MM-DD HH:MM:SS'.
            end_time (str): End time in format 'YYYY-MM-DD HH:MM:SS'.
            fields (str | list[str]): The fields to include in the results list.
            locale_site (str): Locale site, such as 'ru_site' for the Russian site.
            page_no (int): Page number to fetch.
            page_size (int): Number of records per page, up to 50.
            status (str): Status filter for the orders, e.g., 'Payment Completed'.

        Returns:
            OrderListResponse: Contains response information and the list of orders.

        Raises:
            ProductsNotFoundException: If no orders are found for the specified parameters.
            ApiRequestException: If the API request fails.
        """
        request = aliapi.rest.AliexpressAffiliateOrderListRequest()
        request.app_signature = self._app_signature
        request.start_time = start_time
        request.end_time = end_time
        request.fields = ','.join(fields) if isinstance(fields, list) else fields
        request.locale_site = locale_site
        request.page_no = page_no
        request.page_size = page_size
        request.status = status

        response = api_request(request, 'aliexpress_affiliate_order_list_response')

        if response.current_record_count > 0:
            return response
        else:
            raise OrdersNotFoundException("No orders found for the specified parameters")



    def get_ds_product(self,
                       product_id: str,
                       country: str = None,
                       fields: Union[str, List[str]] = None,
                       locale: str = None,
                       web_site: str = None,
                       **kwargs) -> models.DsProductGetResponse:
        """Get detailed information about a dropshipping product.

        Args:
            product_id (str): The product ID.
            country (str): Country code for targeting.
            fields (str | list[str]): Fields to include in the response.
            locale (str): Locale for the request.
            web_site (str): Website identifier.

        Returns:
            models.DsProductGetResponse: Contains product information including base info,
                properties, SKU info, logistics, package, and multimedia info.

        Raises:
            ProductsNotFoundException: If product not found.
            ApiRequestException: If the API request fails.
            ApiRequestResponseException: If the API response is invalid.
        """
        request = aliapi.rest.AliexpressDsProductGetRequest()
        request.app_signature = self._app_signature
        request.country = country
        request.fields = get_list_as_string(fields)
        request.locale = locale
        request.target_currency = self._currency
        request.target_language = self._language
        request.web_site = web_site
        request.product_id = product_id

        response = api_request(request, 'aliexpress_ds_product_get_response')

        return response


    def get_ds_categories(self,
                          country: str = None,
                          fields: Union[str, List[str]] = None,
                          locale: str = None,
                          web_site: str = None,
                          **kwargs) -> models.DsCategoryGetResponse:
        """Get dropshipping categories.

        Args:
            country (str): Country code for targeting.
            fields (str | list[str]): Fields to include in the response.
            locale (str): Locale for the request.
            web_site (str): Website identifier.

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
        request.country = country
        request.fields = get_list_as_string(fields)
        request.locale = locale
        request.target_currency = self._currency
        request.target_language = self._language
        request.web_site = web_site

        response = api_request(request, 'aliexpress_ds_category_get_response')

        return response


    def add_dropshipper(self,
                        email: str,
                        mobile: str = None,
                        app_name: str = None,
                        country: str = None,
                        locale: str = None,
                        platform: str = None,
                        **kwargs):
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

        response = api_request(request, 'ds_dropshpper_add_response')

        return response


    def get_ds_orders(self,
                       start_time: str,
                       end_time: str,
                       status: str = None,
                       fields: Union[str, List[str]] = None,
                       locale: str = None,
                       page_no: int = None,
                       page_size: int = None,
                       **kwargs) -> models.DsOrderListResponse:
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

        response = api_request(request, 'ds_order_list_response')

        if response.current_record_count > 0:
            return response
        else:
            raise OrdersNotFoundException("No orders found for the specified parameters")


    def get_ds_trade_order(self,
                           order_id: str,
                           fields: Union[str, List[str]] = None,
                           locale: str = None,
                           **kwargs) -> models.DsTradeOrderGetResponse:
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

        response = api_request(request, 'aliexpress_ds_trade_order_get_response')

        return response


    def get_ds_commission_orders(self,
                                 start_time: str,
                                 end_time: str,
                                 fields: Union[str, List[str]] = None,
                                 locale: str = None,
                                 page_no: int = None,
                                 page_size: int = None,
                                 **kwargs) -> models.DsCommissionOrderListResponse:
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

        response = api_request(request, 'aliexpress_ds_commissionorder_listbyindex_response')

        if response.current_record_count > 0:
            return response
        else:
            raise OrdersNotFoundException("No commission orders found for the specified parameters")


    def ds_image_search(self,
                        image_id: str,
                        country: str = None,
                        fields: Union[str, List[str]] = None,
                        locale: str = None,
                        web_site: str = None,
                        **kwargs):
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

        response = api_request(request, 'aliexpress_ds_image_search_response')

        return response


    def get_ds_recommend_feed(self,
                              feed_name: str = None,
                              country: str = None,
                              fields: Union[str, List[str]] = None,
                              locale: str = None,
                              page_no: int = None,
                              page_size: int = None,
                              web_site: str = None,
                              **kwargs):
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

        response = api_request(request, 'aliexpress_ds_recommend_feed_get_response')

        return response


    def create_ds_order(self,
                       address: dict,
                       child_order_list: list,
                       locale: str = None,
                       web_site: str = None,
                       **kwargs):
        """Create and pay for a dropshipping order.

        Args:
            address (dict): Shipping address information.
            child_order_list (list): List of child orders with product details.
            locale (str): Locale for the request.
            web_site (str): Website identifier.

        Returns:
            Order creation response.

        Raises:
            ApiRequestException: If the API request fails.
            ApiRequestResponseException: If the API response is invalid.
        """
        request = aliapi.rest.AliexpressDsOrderCreateRequest()
        request.app_signature = self._app_signature
        request.address = str(address)
        request.child_order_list = str(child_order_list)
        request.locale = locale
        request.web_site = web_site

        response = api_request(request, 'aliexpress_ds_order_create_response')

        return response


    def query_ds_freight(self,
                         country_code: str,
                         product_list: list,
                         locale: str = None,
                         web_site: str = None,
                         **kwargs):
        """Query freight/shipping costs for products.

        Args:
            country_code (str): Country code for shipping destination.
            product_list (list): List of products with SKU information.
            locale (str): Locale for the request.
            web_site (str): Website identifier.

        Returns:
            Freight query response.

        Raises:
            ApiRequestException: If the API request fails.
            ApiRequestResponseException: If the API response is invalid.
        """
        request = aliapi.rest.AliexpressDsFreightQueryRequest()
        request.app_signature = self._app_signature
        request.country_code = country_code
        request.locale = locale
        request.product_list = str(product_list)
        request.web_site = web_site

        response = api_request(request, 'aliexpress_ds_freight_query_response')

        return response


    def get_ds_order_tracking(self,
                             order_id: str,
                             locale: str = None,
                             web_site: str = None,
                             **kwargs):
        """Get tracking information for a dropshipping order.

        Args:
            order_id (str): The order ID.
            locale (str): Locale for the request.
            web_site (str): Website identifier.

        Returns:
            Order tracking information.

        Raises:
            OrdersNotFoundException: If order not found.
            ApiRequestException: If the API request fails.
            ApiRequestResponseException: If the API response is invalid.
        """
        request = aliapi.rest.AliexpressDsOrderTrackingGetRequest()
        request.app_signature = self._app_signature
        request.locale = locale
        request.order_id = order_id
        request.web_site = web_site

        response = api_request(request, 'aliexpress_ds_order_tracking_get_response')

        return response


    def get_ds_feed_items(self,
                         feed_name: str,
                         locale: str = None,
                         page_no: int = None,
                         page_size: int = None,
                         web_site: str = None,
                         **kwargs):
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

        response = api_request(request, 'aliexpress_ds_feed_itemids_get_response')

        return response


    def get_ds_product_special_info(self,
                                    product_id: str,
                                    fields: Union[str, List[str]] = None,
                                    locale: str = None,
                                    web_site: str = None,
                                    **kwargs):
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

        response = api_request(request, 'aliexpress_ds_product_specialinfo_get_response')

        return response


    def get_ds_wholesale_product(self,
                                 product_id: str,
                                 fields: Union[str, List[str]] = None,
                                 locale: str = None,
                                 web_site: str = None,
                                 **kwargs):
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

        response = api_request(request, 'aliexpress_ds_product_wholesale_get_response')

        return response


    def calculate_buyer_freight(self,
                                country_code: str,
                                product_list: list,
                                locale: str = None,
                                web_site: str = None,
                                **kwargs):
        """Freight calculation interface provided for buyers.

        Args:
            country_code (str): Country code for shipping destination.
            product_list (list): List of products with SKU information.
            locale (str): Locale for the request.
            web_site (str): Website identifier.

        Returns:
            Freight calculation response.

        Raises:
            ApiRequestException: If the API request fails.
            ApiRequestResponseException: If the API response is invalid.
        """
        request = aliapi.rest.AliexpressLogisticsBuyerFreightCalculateRequest()
        request.app_signature = self._app_signature
        request.country_code = country_code
        request.locale = locale
        request.product_list = str(product_list)
        request.web_site = web_site

        response = api_request(request, 'aliexpress_logistics_buyer_freight_calculate_response')

        return response


    def text_search_ds(self,
                       keywords: str,
                       category_ids: Union[str, List[str]] = None,
                       country: str = None,
                       fields: Union[str, List[str]] = None,
                       locale: str = None,
                       page_no: int = None,
                       page_size: int = None,
                       **kwargs):
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
        request.category_ids = get_list_as_string(category_ids)
        request.country = country
        request.fields = get_list_as_string(fields)
        request.keywords = keywords
        request.locale = locale
        request.page_no = page_no
        request.page_size = page_size
        request.target_currency = self._currency
        request.target_language = self._language
        request.web_site = web_site

        response = api_request(request, 'aliexpress_ds_text_search_response')

        if response.current_record_count > 0:
            return response
        else:
            raise ProductsNotFoudException('No products found with current parameters')


    def report_ds_search_event(self,
                               event_list: list,
                               locale: str = None,
                               web_site: str = None,
                               **kwargs):
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

        response = api_request(request, 'aliexpress_ds_search_event_report_response')

        return response


    def get_ds_member_benefit(self,
                             locale: str = None,
                             web_site: str = None,
                             **kwargs):
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

        response = api_request(request, 'aliexpress_ds_member_benefit_get_response')

        return response


    def get_trade_ds_order(self,
                           order_id: str,
                           fields: Union[str, List[str]] = None,
                           locale: str = None,
                           web_site: str = None,
                           **kwargs):
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

        response = api_request(request, 'aliexpress_trade_ds_order_get_response')

        return response
