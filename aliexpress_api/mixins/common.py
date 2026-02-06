"""Common mixin for AliExpress API.

DEPRECATED: This mixin is kept for backward compatibility only.
Use the service-based API instead:
    >>> api = AliexpressApi(KEY, SECRET)
    >>> api.common.get_products_details(["..."])
"""

from typing import List, Union


class CommonMixin:
    """Mixin providing common API methods.

    DEPRECATED: Use api.common instead of inheriting from this mixin.
    """

    def get_products_details(
        self,
        product_ids: Union[str, List[str]],
        fields: Union[str, List[str]] = None,
        country: str = None,
        **kwargs,
    ):
        """Get products information.

        Delegates to self.common.get_products_details().
        """
        return self.common.get_products_details(
            product_ids=product_ids, fields=fields, country=country, **kwargs
        )

    def get_categories(self, **kwargs):
        """Get all available categories.

        Delegates to self.common.get_categories().
        """
        return self.common.get_categories(**kwargs)

    def get_parent_categories(self, use_cache=True, **kwargs) -> List:
        """Get all available parent categories.

        Delegates to self.common.get_parent_categories().
        """
        return self.common.get_parent_categories(use_cache=use_cache, **kwargs)

    def get_child_categories(self, parent_category_id: int, use_cache=True, **kwargs):
        """Get child categories for a specific parent category.

        Delegates to self.common.get_child_categories().
        """
        return self.common.get_child_categories(
            parent_category_id=parent_category_id, use_cache=use_cache, **kwargs
        )

    def calculate_buyer_freight(
        self,
        country_code: str,
        product_list: list,
        locale: str = None,
        web_site: str = None,
        **kwargs,
    ):
        """Calculate freight/shipping costs for buyers.

        Delegates to self.common.calculate_buyer_freight().
        """
        return self.common.calculate_buyer_freight(
            country_code=country_code,
            product_list=product_list,
            locale=locale,
            web_site=web_site,
            **kwargs,
        )
