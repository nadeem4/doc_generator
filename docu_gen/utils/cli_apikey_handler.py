import os
import logging
from typing import Optional
from docu_gen.utils.apikey_handler import APIKeyHandler

logger = logging.getLogger("docu_gen")

class CLIAPIKeyHandler(APIKeyHandler):
    """Handles API key retrieval from CLI arguments by setting environment variables."""

    def __init__(self, provider_name: str, api_key: Optional[str] = None, successor: Optional[APIKeyHandler] = None):
        """
        Initializes the handler with the provider name, optional API key, and successor.

        Args:
            provider_name (str): The name of the AI provider (e.g., "openai", "anthropic").
            api_key (Optional[str]): The API key provided via CLI argument.
            successor (Optional[APIKeyHandler]): The next handler in the chain.
        """
        super().__init__(successor)
        self.provider_name = provider_name.upper()
        self.api_key = api_key
        logger.debug(f"CLIAPIKeyHandler initialized for provider: {self.provider_name}")

    def handle(self, provider_name: str) -> Optional[str]:
        """
        Sets the API key in the environment variable if provided via CLI.
        If not set, delegates to the successor.

        Args:
            provider_name (str): The name of the AI provider.

        Returns:
            Optional[str]: The API key if set or found, otherwise None.
        """
        if self.api_key:
            env_var_name = f"{self.provider_name}_API_KEY"
            os.environ[env_var_name] = self.api_key
            logger.info(f"Set {env_var_name} from CLI API key argument.")
            return self.api_key
        elif self._successor:
            return self._successor.handle(provider_name)
        else:
            return None
