from typing import List, Optional, Any, Dict


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
    ae_item_base_info: Optional['AeItemBaseInfoDto'] = None
    logistics_info: Optional['LogisticsInfoDto'] = None
    package_info: Optional['PackageInfoDto'] = None
    multimedia_info: Optional['AeMultimediaInfoDto'] = None


class AeItemBaseInfoDto:
    """Basic information about an AliExpress item."""
    subject: str
    detail: str
    mobile_detail: str
    product_id: str
    category_id: str
    product_status_type: str
    currency_code: str
    avg_evaluation_rating: str
    evaluation_count: str
    sales_count: str
    gmt_create: str
    gmt_modified: str
    owner_member_seq_long: str
    category_sequence: Optional[str] = None
    separated_listing: Optional[str] = None


class ItemProperty:
    """Property information for an item."""
    attr_name: str
    attr_value: str
    attr_name_id: Optional[str] = None
    attr_value_id: Optional[str] = None
    attr_value_unit: Optional[str] = None
    attr_value_start: Optional[str] = None
    attr_value_end: Optional[str] = None


class AeItemSkuInfoDto:
    """SKU information for an item."""
    sku_id: str
    id: str  # e.g. "73:175#Black Green;71:193#Polarized"
    sku_price: str
    offer_sale_price: str
    offer_bulk_sale_price: str
    sku_available_stock: str
    sku_bulk_order: str
    currency_code: str
    ean_code: Optional[str] = None
    barcode: Optional[str] = None
    price_include_tax: Optional[str] = None
    tax_amount: Optional[str] = None
    tax_currency_code: Optional[str] = None
    estimated_import_charges: Optional[str] = None
    limit_strategy: Optional[str] = None
    buy_amount_limit_set_by_promotion: Optional[str] = None
    sku_attr: Optional[str] = None
    ae_sku_property_dtos: Optional[List['AeSkuPropertyDto']] = None
    wholesale_price_tiers: Optional[List['WholesalePriceTier']] = None


class AeSkuPropertyDto:
    """SKU property information."""
    sku_property_id: str
    sku_property_name: str
    property_value_id: str
    property_value_definition_name: str
    sku_property_value: str
    sku_image: Optional[str] = None


class WholesalePriceTier:
    """Wholesale price tier information."""
    min_quantity: str
    wholesale_price: str
    discount: str


class LogisticsInfoDto:
    """Logistics information for a product."""
    delivery_time: str
    ship_to_country: str


class PackageInfoDto:
    """Package information for a product."""
    package_length: str
    package_width: str
    package_height: str
    gross_weight: str
    package_type: str
    product_unit: str
    base_unit: str


class AeMultimediaInfoDto:
    """Multimedia information for a product."""
    image_urls: str  # Semicolon separated URLs
    ae_video_dtos: Optional[List['AeVideoDto']] = None


class AeVideoDto:
    """Video information for a product."""
    media_id: str
    media_type: str
    media_status: str
    media_url: str
    poster_url: str
    ali_member_id: str


class StoreInfo:
    """Store information."""
    store_id: str
    store_name: str
    store_country_code: str
    communication_rating: str
    shipping_speed_rating: str
    item_as_described_rating: str


class ManufacturerInfo:
    """Manufacturer information."""
    name: str
    address: str
    phone: str
    phone_prefix: str
    email: str
    country_name: str


class ProductIdConverterResult:
    """Product ID conversion result."""
    main_product_id: str
    sub_product_id: Dict[str, Any]


class DsProductGetResult:
    """Detailed result for product info query."""
    ae_item_base_info_dto: AeItemBaseInfoDto
    ae_multimedia_info_dto: AeMultimediaInfoDto
    ae_item_sku_info_dtos: List[AeItemSkuInfoDto]
    package_info_dto: PackageInfoDto
    logistics_info_dto: LogisticsInfoDto
    ae_store_info: StoreInfo
    ae_item_properties: List[ItemProperty]
    manufacturer_info: Optional[ManufacturerInfo] = None
    product_id_converter_result: Optional[ProductIdConverterResult] = None
    has_whole_sale: Optional[str] = None


class DsProductGetResponse:
    """Response for getting dropshipping product details."""
    result: DsProductGetResult
    code: str
    rsp_code: str
    rsp_msg: str
    request_id: str


class DsCategory:
    """Model for dropshipping category information."""
    category_id: int
    category_name: str
    parent_category_id: Optional[int] = None
    children: Optional[List['DsCategory']] = None


class DsCategoryGetResponse:
    """Response for getting dropshipping categories."""
    categories: List[DsCategory]


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


class DsOrderListResponse:
    """Response for listing dropshipping orders."""
    total_record_count: int
    current_record_count: int
    orders: List[DsOrder]


class DsCommissionOrder:
    """Model for dropshipping commission order information."""
    order_id: str
    commission_status: str
    commission_rate: str
    commission_amount: str
    currency: str
    order_time: str
    affiliate_order_id: Optional[str] = None


class DsCommissionOrderListResponse:
    """Response for listing dropshipping commission orders."""
    total_record_count: int
    current_record_count: int
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


class DsSearchProduct:
    """Product information from search results."""
    itemId: str
    title: str
    itemMainPic: str
    itemUrl: str
    salePrice: str
    salePriceCurrency: str
    originalPrice: Optional[str] = None
    originalPriceCurrency: Optional[str] = None
    discount: Optional[str] = None
    evaluateRate: Optional[str] = None
    orders: Optional[str] = None
    score: Optional[str] = None
    videoUrl: Optional[str] = None


class DsTextSearchResult:
    """Result data for dropshipping text search."""
    totalCount: int
    pageIndex: int
    pageSize: int
    products: List[DsSearchProduct]


class DsTextSearchResponse:
    """Response for dropshipping text search."""
    data: Optional[DsTextSearchResult] = None
    code: Optional[str] = None
    msg: Optional[str] = None

