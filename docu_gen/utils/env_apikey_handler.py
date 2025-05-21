import os
import logging # Import logging
from typing import Optional
from docu_gen.utils.apikey_handler import APIKeyHandler

# Get a logger instance for this module
logger = logging.getLogger("docu_gen")

class EnvAPIKeyHandler(APIKeyHandler):
    """Handles API key retrieval from environment variables."""

    def __init__(self, provider_name: str, successor: Optional[APIKeyHandler] = None):
        """
        Initializes the handler with the provider name and an optional successor.

        Args:
            provider_name (str): The name of the AI provider (e.g., "openai", "anthropic").
            successor (Optional[APIKeyHandler]): The next handler in the chain.
        """
        super().__init__(successor)
        self.provider_name = provider_name.upper() # Store as uppercase for env var convention
        logger.debug(f"EnvAPIKeyHandler initialized for provider: {self.provider_name}")

    def _get_env_var_name(self) -> str:
        """Constructs the environment variable name for the provider's API key."""
        # Standard convention: PROVIDER_API_KEY (e.g., OPENAI_API_KEY)
        return f"{self.provider_name}_API_KEY"

    def handle(self, provider_name: str) -> Optional[str]:
        """
        Handle the request to retrieve an API key from environment variables.
        If not found, delegate to the successor in the chain.

        Args:
            provider_name (str): The name of the AI provider (e.g., "openai", "anthropic").

        Returns:
            Optional[str]: The API key if found, otherwise None.
        """
        env_var_name = self._get_env_var_name()
        key_from_env = os.environ.get(env_var_name)

        if key_from_env:
            logger.info(f"API key for {self.provider_name} retrieved from environment variable ({env_var_name}).")
            # Security note: Be cautious about logging the key itself, even at DEBUG.
            # logger.debug(f"API Key found in env for {self.provider_name}: {'*' * (len(key_from_env) - 4) + key_from_env[-4:] if len(key_from_env) > 4 else '****'}")
            return key_from_env
        else:
            logger.debug(f"API key for {self.provider_name} not found in environment variable {env_var_name}.")
            if self._successor:
                return self._successor.handle(provider_name)
            return None
