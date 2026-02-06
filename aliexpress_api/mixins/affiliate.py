"""Affiliate marketing mixin for AliExpress API.

DEPRECATED: This mixin is kept for backward compatibility only.
Use the service-based API instead:
    >>> api = AliexpressApi(KEY, SECRET)
    >>> api.affiliate.get_affiliate_links(["..."])
"""

from typing import List, Union


class AffiliateMixin:
    """Mixin providing affiliate marketing methods.

    DEPRECATED: Use api.affiliate instead of inheriting from this mixin.
    """

    def get_affiliate_links(
        self, links: Union[str, List[str]], link_type=None, **kwargs
    ):
        """Convert links to affiliate links.

        Delegates to self.affiliate.get_affiliate_links().
        """
        return self.affiliate.get_affiliate_links(
            links=links, link_type=link_type, **kwargs
        )

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
        platform_product_type=None,
        ship_to_country: str = None,
        sort=None,
        **kwargs,
    ):
        """Search for affiliated products with high commission.

        Delegates to self.affiliate.get_hotproducts().
        """
        return self.affiliate.get_hotproducts(
            category_ids=category_ids,
            delivery_days=delivery_days,
            fields=fields,
            keywords=keywords,
            max_sale_price=max_sale_price,
            min_sale_price=min_sale_price,
            page_no=page_no,
            page_size=page_size,
            platform_product_type=platform_product_type,
            ship_to_country=ship_to_country,
            sort=sort,
            **kwargs,
        )

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
        platform_product_type=None,
        ship_to_country: str = None,
        sort=None,
        **kwargs,
    ):
        """Search for affiliated products.

        Delegates to self.affiliate.get_products().
        """
        return self.affiliate.get_products(
            category_ids=category_ids,
            delivery_days=delivery_days,
            fields=fields,
            keywords=keywords,
            max_sale_price=max_sale_price,
            min_sale_price=min_sale_price,
            page_no=page_no,
            page_size=page_size,
            platform_product_type=platform_product_type,
            ship_to_country=ship_to_country,
            sort=sort,
            **kwargs,
        )

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
        **kwargs,
    ):
        """Get affiliated products using smart match.

        Delegates to self.affiliate.smart_match_product().
        """
        return self.affiliate.smart_match_product(
            device_id=device_id,
            app=app,
            country=country,
            device=device,
            fields=fields,
            keywords=keywords,
            page_no=page_no,
            product_id=product_id,
            site=site,
            target_currency=target_currency,
            target_language=target_language,
            tracking_id=tracking_id,
            user=user,
            **kwargs,
        )

    def get_order_list(
        self,
        status: str,
        start_time: str,
        end_time: str,
        fields: Union[str, List[str]] = None,
        locale_site: str = None,
        page_no: int = None,
        page_size: int = None,
        **kwargs,
    ):
        """Retrieve affiliate orders from AliExpress.

        Delegates to self.affiliate.get_order_list().
        """
        return self.affiliate.get_order_list(
            status=status,
            start_time=start_time,
            end_time=end_time,
            fields=fields,
            locale_site=locale_site,
            page_no=page_no,
            page_size=page_size,
            **kwargs,
        )
