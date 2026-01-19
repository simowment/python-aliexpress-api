from dataclasses import dataclass
from .base import BaseModel

@dataclass
class AffiliateLink(BaseModel):
    promotion_link: str = ""
    source_value: str = ""
