from dataclasses import dataclass, field
from typing import List
from .order import Order
from .base import BaseModel

@dataclass
class OrderListResponse(BaseModel):
    total_record_count: int = 0
    current_record_count: int = 0
    total_page_no: int = 0
    current_page_no: int = 0
    orders: List[Order] = field(default_factory=list)