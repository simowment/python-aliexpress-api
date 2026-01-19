import inspect
import json
import os
import sys
from enum import Enum
from typing import get_type_hints, List, Union, Any, Dict, get_args, get_origin

# Add the project root to sys.path to allow importing the local package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from aliexpress_api.api import AliexpressApi
from aliexpress_api.models.base import BaseModel

class OpenAPIGenerator:
    def __init__(self, title="AliExpress SDK API", version="1.0.0"):
        self.spec = {
            "openapi": "3.0.0",
            "info": {
                "title": title,
                "version": version,
                "description": "Auto-generated OpenAPI spec from the python-aliexpress-api SDK."
            },
            "servers": [
                {"url": "https://gw.api.alibaba.com/openapi/rest1", "description": "AliExpress Global API"}
            ],
            "paths": {},
            "components": {
                "schemas": {}
            }
        }
        self.processed_schemas = set()

    def map_python_type_to_openapi(self, python_type: Any) -> Dict[str, Any]:
        origin = get_origin(python_type)
        args = get_args(python_type)

        if python_type is str:
            return {"type": "string"}
        elif python_type is int:
            return {"type": "integer"}
        elif python_type is bool:
            return {"type": "boolean"}
        elif python_type is float:
            return {"type": "number"}
        elif origin is list or origin is List:
            inner_type = args[0] if args else Any
            return {
                "type": "array",
                "items": self.map_python_type_to_openapi(inner_type)
            }
        elif origin is Union:
            # Handle Optional[T] which is Union[T, NoneType]
            # Use type(None) for comparison
            non_none_args = [arg for arg in args if arg is not type(None)]
            if len(non_none_args) == 1:
                return self.map_python_type_to_openapi(non_none_args[0])
            return {"anyOf": [self.map_python_type_to_openapi(arg) for arg in non_none_args]}
        elif inspect.isclass(python_type) and issubclass(python_type, Enum):
            return {
                "type": "string",
                "enum": [e.value for e in python_type]
            }
        elif inspect.isclass(python_type) and issubclass(python_type, BaseModel):
            self.generate_schema(python_type)
            return {"$ref": f"#/components/schemas/{python_type.__name__}"}
        
        return {"type": "string"}  # Default fallback

    def generate_schema(self, model_class: type):
        if model_class.__name__ in self.processed_schemas:
            return
        
        self.processed_schemas.add(model_class.__name__)
        
        schema = {
            "type": "object",
            "properties": {},
            "description": model_class.__doc__.strip() if model_class.__doc__ else ""
        }
        
        hints = get_type_hints(model_class)
        for field_name, field_type in hints.items():
            schema["properties"][field_name] = self.map_python_type_to_openapi(field_type)
            
        self.spec["components"]["schemas"][model_class.__name__] = schema

    def parse_docstring(self, docstring: str) -> str:
        if not docstring:
            return ""
        lines = docstring.strip().split('\n')
        summary = lines[0]
        return summary

    def generate(self):
        # Inspect AliexpressApi methods
        for name, method in inspect.getmembers(AliexpressApi, predicate=inspect.isfunction):
            if name.startswith('_') or name == 'from_dict':
                continue
            
            sig = inspect.signature(method)
            doc = method.__doc__
            summary = self.parse_docstring(doc)
            
            path = f"/{name}"
            self.spec["paths"][path] = {
                "post": {
                    "operationId": name,
                    "summary": summary,
                    "parameters": [],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                        }
                    }
                }
            }
            
            hints = get_type_hints(method)
            
            # Map parameters
            for param_name, param in sig.parameters.items():
                if param_name in ('self', 'kwargs'):
                    continue
                
                param_type = hints.get(param_name, str)
                param_spec = {
                    "name": param_name,
                    "in": "query",
                    "required": param.default is inspect.Parameter.empty,
                    "schema": self.map_python_type_to_openapi(param_type)
                }
                self.spec["paths"][path]["post"]["parameters"].append(param_spec)
                
            # Map return type
            return_type = hints.get('return')
            if return_type:
                # If it's a BaseModel, map it to a ref
                if inspect.isclass(return_type) and issubclass(return_type, BaseModel):
                    self.generate_schema(return_type)
                    self.spec["paths"][path]["post"]["responses"]["200"]["content"] = {
                        "application/json": {
                            "schema": {"$ref": f"#/components/schemas/{return_type.__name__}"}
                        }
                    }
                else:
                    self.spec["paths"][path]["post"]["responses"]["200"]["content"] = {
                        "application/json": {
                            "schema": self.map_python_type_to_openapi(return_type)
                        }
                    }

        return self.spec

if __name__ == "__main__":
    generator = OpenAPIGenerator()
    openapi_spec = generator.generate()
    
    output_file = "openapi.json"
    with open(output_file, "w") as f:
        json.dump(openapi_spec, f, indent=2)
    
    print(f"Successfully generated OpenAPI spec to {output_file}")
