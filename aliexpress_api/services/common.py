"""Common service for AliExpress API.

This module provides common API methods for the AliExpress API.
"""

from typing import List, Union, Optional

from .base import BaseService
from .. import models
from ..sdk import api as aliapi
from ..helpers import api_request, get_list_as_string, get_product_ids
from ..errors import ProductsNotFoundException, CategoriesNotFoundException
from ..helpers.categories import filter_child_categories, filter_parent_categories
from ..models.category import ChildCategory


class CommonService(BaseService):
    """Service providing common API methods.

    Example:
        >>> from aliexpress_api import AliexpressApi
        >>> api = AliexpressApi(KEY, SECRET, tracking_id="YOUR_TRACKING_ID")
        >>> products = api.common.get_products_details(["1005001234567890"])
    """

    def __init__(self, *args, **kwargs):
        """Initialize the common service with category caching."""
        super().__init__(*args, **kwargs)
        self.categories = None

    def get_products_details(
        self,
        product_ids: Union[str, List[str]],
        fields: Union[str, List[str]] = None,
        country: str = None,
    ) -> List[models.Product]:
        """Get detailed information about products.

        Args:
            product_ids: One or more product IDs or URLs.
            fields: Fields to include in results.
            country: Filter products available for this country.

        Returns:
            List of Product objects.

        Raises:
            ProductsNotFoundException: If no products found.
            ApiRequestException: If the request fails.
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
            tracking_id=self._tracking_id,
        )

        response = api_request(
            request,
            "aliexpress_affiliate_productdetail_get_response",
            models.Product,
        )

        if response:
            return response
        else:
            raise ProductsNotFoundException("No products found with current parameters")

    def get_categories(self) -> List[Union[models.Category, ChildCategory]]:
        """Get all available categories.

        Returns:
            List of Category and ChildCategory objects.

        Raises:
            CategoriesNotFoundException: If no categories found.
            ApiRequestException: If the request fails.
        """
        request = self._prepare_request(
            aliapi.rest.AliexpressAffiliateCategoryGetRequest(),
        )

        response = api_request(
            request,
            "aliexpress_affiliate_category_get_response",
            models.Category,
        )

        if response:
            self.categories = response
            return self.categories
        else:
            raise CategoriesNotFoundException("No categories found")

    def get_parent_categories(
        self,
        use_cache: bool = True,
    ) -> List[models.Category]:
        """Get all available parent categories.

        Args:
            use_cache: Use cached categories to reduce API requests.

        Returns:
            List of parent Category objects.

        Raises:
            CategoriesNotFoundException: If no categories found.
            ApiRequestException: If the request fails.
        """
        if not use_cache or not self.categories:
            self.get_categories()
        return filter_parent_categories(self.categories)

    def get_child_categories(
        self,
        parent_category_id: int,
        use_cache: bool = True,
    ) -> List[ChildCategory]:
        """Get child categories for a specific parent category.

        Args:
            parent_category_id: The parent category ID.
            use_cache: Use cached categories to reduce API requests.

        Returns:
            List of ChildCategory objects.

        Raises:
            CategoriesNotFoundException: If no categories found.
            ApiRequestException: If the request fails.
        """
        if not use_cache or not self.categories:
            self.get_categories()
        return filter_child_categories(self.categories, parent_category_id)

    def calculate_buyer_freight(
        self,
        country_code: str,
        product_list: list,
        locale: str = None,
        web_site: str = None,
    ):
        """Calculate freight/shipping costs for buyers.

        Args:
            country_code: Country code for shipping destination.
            product_list: List of products with SKU information.
            locale: Locale for the request.
            web_site: Website identifier.

        Returns:
            Freight calculation response.

        Raises:
            ApiRequestException: If the request fails.
        """
        request = self._prepare_request(
            aliapi.rest.AliexpressLogisticsBuyerFreightCalculateRequest(),
            country_code=country_code,
            locale=locale or f"{str(self._language).lower()}_{country_code.upper()}",
            product_list=str(product_list),
            web_site=web_site,
        )

        response = api_request(
            request,
            "aliexpress_logistics_buyer_freight_calculate_response",
            models.BuyerFreightCalculateResponse,
        )

        return response
