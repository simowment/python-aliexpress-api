from dataclasses import dataclass
from .base import BaseModel

@dataclass
class Category(BaseModel):
    category_id: int = 0
    category_name: str = ""


@dataclass
class ChildCategory(Category):
    parent_category_id: int = 0
