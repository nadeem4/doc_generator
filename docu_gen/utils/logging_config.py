"""Configure logging for the docu-gen package."""

import logging
import sys
from typing import Optional

# Define a custom log level for successful operations, if desired
# SUCCESS = 25  # Between INFO and WARNING
# logging.addLevelName(SUCCESS, "SUCCESS")

# def success(self, message, *args, **kws):
#     if self.isEnabledFor(SUCCESS):
#         self._log(SUCCESS, message, args, **kws)

# logging.Logger.success = success

def setup_logging(level: Optional[str] = "INFO", verbose: bool = False) -> None:
    """Set up logging configuration for the docu-gen package.

    Args:
        level: The logging level to use (e.g., "DEBUG", "INFO", "WARNING").
        verbose: If True, sets level to DEBUG, overriding the 'level' argument.
    """
    logger = logging.getLogger("docu_gen")

    if verbose:
        effective_level = logging.DEBUG
    else:
        effective_level = getattr(logging, level.upper(), logging.INFO)
    
    logger.setLevel(effective_level)

    # Remove existing handlers to avoid duplicate logs if this function is called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    
    # Set formatter
    # For DEBUG level, include more detailed info
    if effective_level == logging.DEBUG:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s')
    else:
        formatter = logging.Formatter('%(levelname)s: %(message)s')
        
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)

    # Prevent log propagation to the root logger if it's not desired
    logger.propagate = False
