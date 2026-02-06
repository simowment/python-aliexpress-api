"""Dropshipping mixin for AliExpress API.

DEPRECATED: This mixin is kept for backward compatibility only.
Use the service-based API instead:
    >>> api = AliexpressApi(KEY, SECRET, token="...")
    >>> api.dropshipping.get_ds_product("...", "US")
"""

from typing import List, Union, Optional


class DropshippingMixin:
    """Mixin providing dropshipping methods.

    DEPRECATED: Use api.dropshipping instead of inheriting from this mixin.
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
        **kwargs,
    ):
        """Get detailed information about a dropshipping product.

        Delegates to self.dropshipping.get_ds_product().
        """
        return self.dropshipping.get_ds_product(
            product_id=product_id,
            ship_to_country=ship_to_country,
            target_currency=target_currency,
            target_language=target_language,
            remove_personal_benefit=remove_personal_benefit,
            biz_model=biz_model,
            province_code=province_code,
            city_code=city_code,
            locale=locale,
            **kwargs,
        )

    def get_ds_categories(
        self, category_id: str = None, language: str = None, **kwargs
    ):
        """Get dropshipping categories.

        Delegates to self.dropshipping.get_ds_categories().
        """
        return self.dropshipping.get_ds_categories(
            category_id=category_id, language=language, **kwargs
        )

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

        Delegates to self.dropshipping.add_dropshipper().
        """
        return self.dropshipping.add_dropshipper(
            email=email,
            mobile=mobile,
            app_name=app_name,
            country=country,
            locale=locale,
            platform=platform,
            **kwargs,
        )

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
    ):
        """Get list of dropshipping orders.

        Delegates to self.dropshipping.get_ds_orders().
        """
        return self.dropshipping.get_ds_orders(
            start_time=start_time,
            end_time=end_time,
            status=status,
            fields=fields,
            locale=locale,
            page_no=page_no,
            page_size=page_size,
            **kwargs,
        )

    def get_ds_trade_order(
        self,
        order_id: str,
        fields: Union[str, List[str]] = None,
        locale: str = None,
        **kwargs,
    ):
        """Get detailed dropshipping trade order information.

        Delegates to self.dropshipping.get_ds_trade_order().
        """
        return self.dropshipping.get_ds_trade_order(
            order_id=order_id, fields=fields, locale=locale, **kwargs
        )

    def get_ds_commission_orders(
        self,
        start_time: str,
        end_time: str,
        fields: Union[str, List[str]] = None,
        locale: str = None,
        page_no: int = None,
        page_size: int = None,
        **kwargs,
    ):
        """Get dropshipping commission orders.

        Delegates to self.dropshipping.get_ds_commission_orders().
        """
        return self.dropshipping.get_ds_commission_orders(
            start_time=start_time,
            end_time=end_time,
            fields=fields,
            locale=locale,
            page_no=page_no,
            page_size=page_size,
            **kwargs,
        )

    def ds_image_search(
        self,
        image_bytes: bytes,
        sort: str = "default",
        search_type: int = 0,
        limit: int = 20,
        target_currency: str = None,
        target_language: str = None,
        **kwargs,
    ):
        """Search products using an image (V2).

        Delegates to self.dropshipping.ds_image_search().
        """
        return self.dropshipping.ds_image_search(
            image_bytes=image_bytes,
            sort=sort,
            search_type=search_type,
            limit=limit,
            target_currency=target_currency,
            target_language=target_language,
            **kwargs,
        )

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

        Delegates to self.dropshipping.get_ds_recommend_feed().
        """
        return self.dropshipping.get_ds_recommend_feed(
            feed_name=feed_name,
            country=country,
            fields=fields,
            locale=locale,
            page_no=page_no,
            page_size=page_size,
            web_site=web_site,
            **kwargs,
        )

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

        Delegates to self.dropshipping.create_ds_order().
        """
        return self.dropshipping.create_ds_order(
            logistics_address=logistics_address,
            product_items=product_items,
            locale=locale,
            out_order_id=out_order_id,
            ds_extend_params=ds_extend_params,
            **kwargs,
        )

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

        Delegates to self.dropshipping.query_ds_freight().
        """
        return self.dropshipping.query_ds_freight(
            product_id=product_id,
            sku_id=sku_id,
            country_code=country_code,
            quantity=quantity,
            locale=locale,
            currency=currency,
            province_code=province_code,
            city_code=city_code,
            language=language,
            **kwargs,
        )

    def get_ds_order_tracking(self, ae_order_id: str, language: str = None, **kwargs):
        """Get dropshipping order tracking information.

        Delegates to self.dropshipping.get_ds_order_tracking().
        """
        return self.dropshipping.get_ds_order_tracking(
            ae_order_id=ae_order_id, language=language, **kwargs
        )

    def get_ds_feed_items(
        self,
        feed_name: str,
        locale: str = None,
        page_no: int = None,
        page_size: int = None,
        web_site: str = None,
        **kwargs,
    ):
        """Fetch items with feed name.

        Delegates to self.dropshipping.get_ds_feed_items().
        """
        return self.dropshipping.get_ds_feed_items(
            feed_name=feed_name,
            locale=locale,
            page_no=page_no,
            page_size=page_size,
            web_site=web_site,
            **kwargs,
        )

    def get_ds_product_special_info(
        self,
        product_id: str,
        fields: Union[str, List[str]] = None,
        locale: str = None,
        web_site: str = None,
        **kwargs,
    ):
        """Get special product information like certification.

        Delegates to self.dropshipping.get_ds_product_special_info().
        """
        return self.dropshipping.get_ds_product_special_info(
            product_id=product_id,
            fields=fields,
            locale=locale,
            web_site=web_site,
            **kwargs,
        )

    def get_ds_wholesale_product(
        self,
        product_id: str,
        fields: Union[str, List[str]] = None,
        locale: str = None,
        web_site: str = None,
        **kwargs,
    ):
        """Get product info for wholesale business.

        Delegates to self.dropshipping.get_ds_wholesale_product().
        """
        return self.dropshipping.get_ds_wholesale_product(
            product_id=product_id,
            fields=fields,
            locale=locale,
            web_site=web_site,
            **kwargs,
        )

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
    ):
        """Text search for dropshipping products.

        Delegates to self.dropshipping.text_search_ds().
        """
        return self.dropshipping.text_search_ds(
            keywords=keywords,
            country=country,
            category_ids=category_ids,
            locale=locale,
            sort=sort,
            page_no=page_no,
            page_size=page_size,
            min_price=min_price,
            max_price=max_price,
            **kwargs,
        )

    def report_ds_search_event(
        self, event_list: list, locale: str = None, web_site: str = None, **kwargs
    ):
        """Report search events for analytics.

        Delegates to self.dropshipping.report_ds_search_event().
        """
        return self.dropshipping.report_ds_search_event(
            event_list=event_list, locale=locale, web_site=web_site, **kwargs
        )

    def get_ds_member_benefit(self, locale: str = None, web_site: str = None, **kwargs):
        """Get dropshipper member benefits.

        Delegates to self.dropshipping.get_ds_member_benefit().
        """
        return self.dropshipping.get_ds_member_benefit(
            locale=locale, web_site=web_site, **kwargs
        )

    def get_trade_ds_order(
        self,
        order_id: str,
        fields: Union[str, List[str]] = None,
        locale: str = None,
        web_site: str = None,
        **kwargs,
    ):
        """Buyer query order details.

        Delegates to self.dropshipping.get_trade_ds_order().
        """
        return self.dropshipping.get_trade_ds_order(
            order_id=order_id, fields=fields, locale=locale, web_site=web_site, **kwargs
        )
