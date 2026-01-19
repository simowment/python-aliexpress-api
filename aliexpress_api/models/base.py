from dataclasses import dataclass
from typing import Any, Dict, List, Type, TypeVar

T = TypeVar("T", bound="BaseModel")

@dataclass
class BaseModel:
    """Base class for all models, with a from_dict method."""
    
    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        if not data or not isinstance(data, dict):
            return cls()  # Fallback to empty instance if data is not a dict
        
        # Get all field names from the dataclass
        fields = {f.name for f in cls.__dataclass_fields__.values()}
        
        # Filter data to only include valid fields
        filtered_data = {}
        for k, v in data.items():
            if k in fields:
                # Handle nested models if needed
                field_type = cls.__dataclass_fields__[k].type
                
                # Basic support for nesting: if it's a list of models or a single model
                # This can be expanded as needed.
                if hasattr(field_type, "__origin__") and field_type.__origin__ is list:
                    inner_type = field_type.__args__[0]
                    if isinstance(inner_type, type) and issubclass(inner_type, BaseModel):
                        filtered_data[k] = [inner_type.from_dict(i) for i in v] if isinstance(v, list) else []
                    else:
                        filtered_data[k] = v
                elif isinstance(field_type, type) and issubclass(field_type, BaseModel):
                    filtered_data[k] = field_type.from_dict(v) if isinstance(v, dict) else None
                else:
                    filtered_data[k] = v
                    
        return cls(**filtered_data)
