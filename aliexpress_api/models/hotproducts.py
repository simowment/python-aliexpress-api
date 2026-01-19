from dataclasses import dataclass, field
from typing import List
from .product import Product
from .base import BaseModel


@dataclass
class HotProductsResponse(BaseModel):
    current_page_no: int = 0
    current_record_count: int = 0
    total_record_count: int = 0
    products: List[Product] = field(default_factory=list)
