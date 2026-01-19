from dataclasses import dataclass, field
from typing import List
from .base import BaseModel


@dataclass
class Product(BaseModel):
    app_sale_price: str = ""
    app_sale_price_currency: str = ""
    commission_rate: str = ""
    discount: str = ""
    evaluate_rate: str = ""
    first_level_category_id: int = 0
    first_level_category_name: str = ""
    lastest_volume: int = 0
    hot_product_commission_rate: str = ""
    original_price: str = ""
    original_price_currency: str = ""
    product_detail_url: str = ""
    product_id: int = 0
    product_main_image_url: str = ""
    product_small_image_urls: List[str] = field(default_factory=list)
    product_title: str = ""
    product_video_url: str = ""
    promotion_link: str = ""
    relevant_market_commission_rate: str = ""
    sale_price: str = ""
    sale_price_currency: str = ""
    second_level_category_id: int = 0
    second_level_category_name: str = ""
    shop_id: int = 0
    shop_url: str = ""
    target_app_sale_price: str = ""
    target_app_sale_price_currency: str = ""
    target_original_price: str = ""
    target_original_price_currency: str = ""
    target_sale_price: str = ""
    target_sale_price_currency: str = ""


@dataclass
class ProductsResponse(BaseModel):
    current_page_no: int = 0
    current_record_count: int = 0
    total_record_count: int = 0
    products: List[Product] = field(default_factory=list)
