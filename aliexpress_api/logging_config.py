"""Logging configuration for AliExpress API.

This module provides a centralized logging configuration that can be
controlled via environment variables or programmatically.

Usage:
    # Enable debug logging programmatically
    from aliexpress_api import set_debug_mode
    set_debug_mode(True)
    
    # Or via environment variable
    # Set ALIEXPRESS_API_DEBUG=1 before importing

    # Get logger for use in other modules
    from aliexpress_api.logging_config import get_logger
    logger = get_logger(__name__)
    logger.debug("This is a debug message")
"""

import logging
import os
import sys

# Logger name for the entire package
LOGGER_NAME = "aliexpress_api"

# Check environment variable for debug mode
_debug_mode = os.environ.get("ALIEXPRESS_API_DEBUG", "").lower() in ("1", "true", "yes")


def get_logger(name: str = None) -> logging.Logger:
    """Get a logger instance for the AliExpress API.
    
    Args:
        name: Optional name for the logger. If None, returns the root package logger.
              If provided, returns a child logger (e.g., 'aliexpress_api.sdk').
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    if name:
        # Create child logger under the package namespace
        if not name.startswith(LOGGER_NAME):
            name = f"{LOGGER_NAME}.{name}"
        return logging.getLogger(name)
    return logging.getLogger(LOGGER_NAME)


def set_debug_mode(enabled: bool = True) -> None:
    """Enable or disable debug mode for the AliExpress API.
    
    When enabled, all API requests and responses will be logged at DEBUG level.
    
    Args:
        enabled: Whether to enable debug mode. Defaults to True.
    
    Example:
        >>> from aliexpress_api import set_debug_mode
        >>> set_debug_mode(True)  # Enable debug logging
        >>> # Make API calls - they will now show debug output
        >>> set_debug_mode(False)  # Disable debug logging
    """
    global _debug_mode
    _debug_mode = enabled
    
    logger = get_logger()
    
    if enabled:
        logger.setLevel(logging.DEBUG)
        # Add handler if not already present
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                "[%(asctime)s] %(name)s %(levelname)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
    else:
        logger.setLevel(logging.WARNING)


def is_debug_mode() -> bool:
    """Check if debug mode is currently enabled.
    
    Returns:
        bool: True if debug mode is enabled, False otherwise.
    """
    return _debug_mode


# Initialize logger on module load
_root_logger = get_logger()
if _debug_mode:
    set_debug_mode(True)
else:
    # Default: only warnings and above
    _root_logger.setLevel(logging.WARNING)

