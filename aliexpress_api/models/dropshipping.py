from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict
from .base import BaseModel


@dataclass
class AeItemBaseInfoDto(BaseModel):
    """Basic information about an AliExpress item."""
    subject: str = ""
    detail: str = ""
    mobile_detail: str = ""
    product_id: str = ""
    category_id: str = ""
    product_status_type: str = ""
    currency_code: str = ""
    avg_evaluation_rating: str = ""
    evaluation_count: str = ""
    sales_count: str = ""
    gmt_create: str = ""
    gmt_modified: str = ""
    owner_member_seq_long: str = ""
    category_sequence: Optional[str] = None
    separated_listing: Optional[str] = None


@dataclass
class ItemProperty(BaseModel):
    """Property information for an item."""
    attr_name: str = ""
    attr_value: str = ""
    attr_name_id: Optional[str] = None
    attr_value_id: Optional[str] = None
    attr_value_unit: Optional[str] = None
    attr_value_start: Optional[str] = None
    attr_value_end: Optional[str] = None


@dataclass
class AeSkuPropertyDto(BaseModel):
    """SKU property information."""
    sku_property_id: str = ""
    sku_property_name: str = ""
    property_value_id: str = ""
    property_value_definition_name: str = ""
    sku_property_value: str = ""
    sku_image: Optional[str] = None


@dataclass
class WholesalePriceTier(BaseModel):
    """Wholesale price tier information."""
    min_quantity: str = ""
    wholesale_price: str = ""
    discount: str = ""


@dataclass
class AeItemSkuInfoDto(BaseModel):
    """SKU information for an item."""
    sku_id: str = ""
    id: str = ""  # e.g. "73:175#Black Green;71:193#Polarized"
    sku_price: str = ""
    offer_sale_price: str = ""
    offer_bulk_sale_price: str = ""
    sku_available_stock: str = ""
    sku_bulk_order: str = ""
    currency_code: str = ""
    ean_code: Optional[str] = None
    barcode: Optional[str] = None
    price_include_tax: Optional[str] = None
    tax_amount: Optional[str] = None
    tax_currency_code: Optional[str] = None
    estimated_import_charges: Optional[str] = None
    limit_strategy: Optional[str] = None
    buy_amount_limit_set_by_promotion: Optional[str] = None
    sku_attr: Optional[str] = None
    ae_sku_property_dtos: List[AeSkuPropertyDto] = field(default_factory=list)
    wholesale_price_tiers: List[WholesalePriceTier] = field(default_factory=list)


@dataclass
class LogisticsInfoDto(BaseModel):
    """Logistics information for a product."""
    delivery_time: str = ""
    ship_to_country: str = ""


@dataclass
class PackageInfoDto(BaseModel):
    """Package information for a product."""
    package_length: str = ""
    package_width: str = ""
    package_height: str = ""
    gross_weight: str = ""
    package_type: str = ""
    product_unit: str = ""
    base_unit: str = ""


@dataclass
class AeVideoDto(BaseModel):
    """Video information for a product."""
    media_id: str = ""
    media_type: str = ""
    media_status: str = ""
    media_url: str = ""
    poster_url: str = ""
    ali_member_id: str = ""


@dataclass
class AeMultimediaInfoDto(BaseModel):
    """Multimedia information for a product."""
    image_urls: str = ""  # Semicolon separated URLs
    ae_video_dtos: List[AeVideoDto] = field(default_factory=list)


@dataclass
class StoreInfo(BaseModel):
    """Store information."""
    store_id: str = ""
    store_name: str = ""
    store_country_code: str = ""
    communication_rating: str = ""
    shipping_speed_rating: str = ""
    item_as_described_rating: str = ""


@dataclass
class ManufacturerInfo(BaseModel):
    """Manufacturer information."""
    name: str = ""
    address: str = ""
    phone: str = ""
    phone_prefix: str = ""
    email: str = ""
    country_name: str = ""


@dataclass
class ProductIdConverterResult(BaseModel):
    """Product ID conversion result."""
    main_product_id: str = ""
    sub_product_id: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DsProductGetResult(BaseModel):
    """Detailed result for product info query."""
    ae_item_base_info_dto: AeItemBaseInfoDto = field(default_factory=AeItemBaseInfoDto)
    ae_multimedia_info_dto: AeMultimediaInfoDto = field(default_factory=AeMultimediaInfoDto)
    ae_item_sku_info_dtos: List[AeItemSkuInfoDto] = field(default_factory=list)
    package_info_dto: PackageInfoDto = field(default_factory=PackageInfoDto)
    logistics_info_dto: LogisticsInfoDto = field(default_factory=LogisticsInfoDto)
    ae_store_info: StoreInfo = field(default_factory=StoreInfo)
    ae_item_properties: List[ItemProperty] = field(default_factory=list)
    manufacturer_info: Optional[ManufacturerInfo] = None
    product_id_converter_result: Optional[ProductIdConverterResult] = None
    has_whole_sale: Optional[str] = None


@dataclass
class DsProductGetResponse(BaseModel):
    """Response for getting dropshipping product details."""
    result: DsProductGetResult = field(default_factory=DsProductGetResult)
    code: str = ""
    rsp_code: str = ""
    rsp_msg: str = ""
    request_id: str = ""


@dataclass
class DsCategory(BaseModel):
    """Model for dropshipping category information."""
    category_id: int = 0
    category_name: str = ""
    parent_category_id: Optional[int] = None
    children: List['DsCategory'] = field(default_factory=list)


@dataclass
class DsCategoryGetResponse(BaseModel):
    """Response for getting dropshipping categories."""
    categories: List[DsCategory] = field(default_factory=list)


@dataclass
class DsOrderProduct(BaseModel):
    """Product information within a dropshipping order."""
    product_id: str = ""
    product_name: str = ""
    sku_id: str = ""
    sku_info: str = ""
    product_count: int = 0
    product_price: str = ""
    product_image_url: str = ""


@dataclass
class DsOrder(BaseModel):
    """Model for dropshipping order information."""
    order_id: str = ""
    order_status: str = ""
    gmt_create: str = ""
    gmt_modified: str = ""
    total_amount: str = ""
    currency: str = ""
    product_count: int = 0
    order_products: List[DsOrderProduct] = field(default_factory=list)


@dataclass
class DsOrderListResponse(BaseModel):
    """Response for listing dropshipping orders."""
    total_record_count: int = 0
    current_record_count: int = 0
    orders: List[DsOrder] = field(default_factory=list)


@dataclass
class DsCommissionOrder(BaseModel):
    """Model for dropshipping commission order information."""
    order_id: str = ""
    commission_status: str = ""
    commission_rate: str = ""
    commission_amount: str = ""
    currency: str = ""
    order_time: str = ""
    affiliate_order_id: Optional[str] = None


@dataclass
class DsCommissionOrderListResponse(BaseModel):
    """Response for listing dropshipping commission orders."""
    total_record_count: int = 0
    current_record_count: int = 0
    commission_orders: List[DsCommissionOrder] = field(default_factory=list)


@dataclass
class OrderLogisticsInfo(BaseModel):
    """Logistics information for an order."""
    logistics_number: str = ""
    logistics_company_name: str = ""
    logistics_status: str = ""


@dataclass
class DsTradeOrderGetResponse(BaseModel):
    """Response for getting dropshipping trade order details."""
    order_id: str = ""
    order_status: str = ""
    gmt_create: str = ""
    gmt_modified: str = ""
    total_amount: str = ""
    currency: str = ""
    product_count: int = 0
    order_products: List[DsOrderProduct] = field(default_factory=list)
    order_logistics_info: List[OrderLogisticsInfo] = field(default_factory=list)


@dataclass
class DsSearchProduct(BaseModel):
    """Product information from search results."""
    itemId: str = ""
    title: str = ""
    itemMainPic: str = ""
    itemUrl: str = ""
    salePrice: str = ""
    salePriceCurrency: str = ""
    originalPrice: Optional[str] = None
    originalPriceCurrency: Optional[str] = None
    discount: Optional[str] = None
    evaluateRate: Optional[str] = None
    orders: Optional[str] = None
    score: Optional[str] = None
    videoUrl: Optional[str] = None


@dataclass
class DsTextSearchResult(BaseModel):
    """Result data for dropshipping text search."""
    totalCount: int = 0
    pageIndex: int = 0
    pageSize: int = 0
    products: List[DsSearchProduct] = field(default_factory=list)


@dataclass
class DsTextSearchResponse(BaseModel):
    """Response for dropshipping text search."""
    data: Optional[DsTextSearchResult] = None
    code: Optional[str] = None
    msg: Optional[str] = None

