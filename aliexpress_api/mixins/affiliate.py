from typing import List, Union
from .. import models
from ..skd import api as aliapi
from ..helpers import api_request, parse_products, get_list_as_string
from ..errors import ProductsNotFoundException, InvalidTrackingIdException, OrdersNotFoundException

class AffiliateMixin:
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
            ``ProductsNotFoundException``
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
            raise ProductsNotFoundException('Affiliate links not available')


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
            ``ProductsNotFoundException``
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
            raise ProductsNotFoundException('No products found with current parameters')


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
            ``ProductsNotFoundException``
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
            raise ProductsNotFoundException('No products found with current parameters')


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
            raise ProductsNotFoundException('No products found with current parameters')
        
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
