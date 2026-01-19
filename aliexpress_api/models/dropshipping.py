from typing import List, Optional


class DsProduct:
    """Model for dropshipping product information."""
    product_id: str
    subject: str
    detail_url: str
    image_url: str
    original_price: str
    sale_price: str
    discount: str
    inventory: int
    shop_id: int
    shop_url: str
    shop_name: str
    ae_item_base_info: Optional['AeItemBaseInfo'] = None
    logistics_info: Optional['LogisticsInfo'] = None
    package_info: Optional['PackageInfo'] = None
    multimedia_info: Optional['MultimediaInfo'] = None


class AeItemBaseInfo:
    """Basic information about an AliExpress item."""
    product_id: str
    subject: str
    detail_url: str
    image_url: str
    original_price: str
    sale_price: str
    discount: str
    inventory: int
    shop_id: int
    shop_url: str


class AeItemProperty:
    """Property information for an item."""
    name: str
    value: str


class AeItemSkuInfo:
    """SKU information for an item."""
    sku_id: str
    sku_price: str
    sku_original_price: str
    sku_discount: str
    available: bool
    inventory: int
    ae_sku_property: List['AeSkuProperty']


class AeSkuProperty:
    """SKU property information."""
    property_id: str
    property_name: str
    property_value_id: str
    property_value_name: str
    property_value_image: Optional[str] = None


class LogisticsInfo:
    """Logistics information for a product."""
    delivery_day: str
    shipping_company_name: str
    location_country: str
    freight_type: str


class PackageInfo:
    """Package information for a product."""
    package_length: str
    package_width: str
    package_height: str
    package_weight: str


class MultimediaInfo:
    """Multimedia information for a product."""
    ae_video: Optional['AeVideo'] = None
    market_image: Optional[List['MarketImage']] = None


class AeVideo:
    """Video information for a product."""
    video_url: str
    video_duration: str


class MarketImage:
    """Market image for a product."""
    image_url: str
    image_size: str


class DsCategory:
    """Model for dropshipping category information."""
    category_id: int
    category_name: str
    parent_category_id: Optional[int] = None
    children: Optional[List['DsCategory']] = None


class DsOrder:
    """Model for dropshipping order information."""
    order_id: str
    order_status: str
    gmt_create: str
    gmt_modified: str
    total_amount: str
    currency: str
    product_count: int
    order_products: Optional[List['DsOrderProduct']] = None


class DsOrderProduct:
    """Product information within a dropshipping order."""
    product_id: str
    product_name: str
    sku_id: str
    sku_info: str
    product_count: int
    product_price: str
    product_image_url: str


class DsCommissionOrder:
    """Model for dropshipping commission order information."""
    order_id: str
    commission_status: str
    commission_rate: str
    commission_amount: str
    currency: str
    order_time: str
    affiliate_order_id: Optional[str] = None


class DsResponse:
    """Base response model for dropshipping endpoints."""
    resp_code: int
    resp_msg: str
    resp_result: Optional['DsResult'] = None


class DsResult:
    """Result container for dropshipping responses."""
    total_record_count: int
    current_record_count: int


class DsProductGetResponse(DsResult):
    """Response for getting dropshipping product details."""
    ae_item_base_info: Optional[AeItemBaseInfo] = None
    ae_item_property: Optional[List[AeItemProperty]] = None
    ae_item_sku_info: Optional[List[AeItemSkuInfo]] = None
    logistics_info: Optional[LogisticsInfo] = None
    package_info: Optional[PackageInfo] = None
    multimedia_info: Optional[MultimediaInfo] = None


class DsCategoryGetResponse(DsResult):
    """Response for getting dropshipping categories."""
    categories: List[DsCategory]


class DsOrderListResponse(DsResult):
    """Response for listing dropshipping orders."""
    orders: List[DsOrder]


class DsCommissionOrderListResponse(DsResult):
    """Response for listing dropshipping commission orders."""
    commission_orders: List[DsCommissionOrder]


class DsTradeOrderGetResponse:
    """Response for getting dropshipping trade order details."""
    order_id: str
    order_status: str
    gmt_create: str
    gmt_modified: str
    total_amount: str
    currency: str
    product_count: int
    order_products: List[DsOrderProduct]
    order_logistics_info: Optional[List['OrderLogisticsInfo']] = None


class OrderLogisticsInfo:
    """Logistics information for an order."""
    logistics_number: str
    logistics_company_name: str
    logistics_status: str
