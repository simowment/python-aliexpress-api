"""Shim module to expose the SDK package under libs.aliexpress_api."""

from .aliexpress_api import AliexpressApi
from .aliexpress_api import models
from .aliexpress_api.logging_config import set_debug_mode, is_debug_mode

__all__ = ["AliexpressApi", "models", "set_debug_mode", "is_debug_mode"]
