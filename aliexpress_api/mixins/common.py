from typing import List, Union
from .. import models
from ..sdk import api as aliapi
from ..helpers import api_request, parse_products, get_list_as_string, get_product_ids
from ..errors import ProductsNotFoundException, CategoriesNotFoundException
from ..helpers.categories import filter_child_categories, filter_parent_categories
from ..models.category import ChildCategory

class CommonMixin:
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
            ``ProductsNotFoundException``
            ``InvalidArgumentException``
            ``ApiRequestException``
            ``ApiRequestResponseException``
        """
        product_ids = get_product_ids(product_ids)
        product_ids = get_list_as_string(product_ids)

        request = self._prepare_request(
            aliapi.rest.AliexpressAffiliateProductdetailGetRequest(),
            fields=get_list_as_string(fields),
            product_ids=product_ids,
            country=country,
            target_currency=self._currency,
            target_language=str(self._language).lower(),
            tracking_id=self._tracking_id
        )

        response = api_request(request, 'aliexpress_affiliate_productdetail_get_response', models.Product)

        if response:
            return response
        else:
            raise ProductsNotFoundException('No products found with current parameters')


    def get_categories(self, **kwargs) -> List[Union[models.Category, ChildCategory]]:
        """Get all available categories, both parent and child.

        Returns:
            ``list[models.Category | models.ChildCategory]``: A list of categories.

        Raises:
            ``CategoriesNotFoundException``
            ``ApiRequestException``
            ``ApiRequestResponseException``
        """
        request = self._prepare_request(
            aliapi.rest.AliexpressAffiliateCategoryGetRequest()
        )

        response = api_request(request, 'aliexpress_affiliate_category_get_response', models.Category)

        if response:
            self.categories = response
            return self.categories
        else:
            raise CategoriesNotFoundException('No categories found')


    def get_parent_categories(self, use_cache=True, **kwargs) -> List[models.Category]:
        """Get all available parent categories.

        Args:
            use_cache (``bool``): Uses cached categories to reduce API requests.

        Returns:
            ``list[models.Category]``: A list of parent categories.

        Raises:
            ``CategoriesNotFoundException``
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
            ``CategoriesNotFoundException``
            ``ApiRequestException``
            ``ApiRequestResponseException``
        """
        if not use_cache or not self.categories:
            self.get_categories()
        return filter_child_categories(self.categories, parent_category_id)

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
        request = self._prepare_request(
            aliapi.rest.AliexpressLogisticsBuyerFreightCalculateRequest(),
            country_code=country_code,
            locale=locale or f"{str(self._language).lower()}_{country_code.upper()}",
            product_list=str(product_list),
            web_site=web_site
        )

        response = api_request(
            request, 
            'aliexpress_logistics_buyer_freight_calculate_response',
            models.BuyerFreightCalculateResponse
        )

        return response

        return response
