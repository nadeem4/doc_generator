import os
import logging # Import logging
from typing import Optional
from azure.identity import DefaultAzureCredential, CredentialUnavailableError
from azure.keyvault.secrets import SecretClient, ResourceNotFoundError
from docu_gen.utils.apikey_handler import APIKeyHandler

# Get a logger instance for this module
logger = logging.getLogger("docu_gen")

class AzureKeyVaultAPIKeyHandler(APIKeyHandler):
    """Handles API key retrieval from Azure Key Vault."""

    def __init__(self, provider_name: str, successor: Optional[APIKeyHandler] = None):
        """
        Initializes the handler with the provider name and an optional successor.

        Args:
            provider_name (str): The name of the AI provider (e.g., "openai", "anthropic").
            successor (Optional[APIKeyHandler]): The next handler in the chain.
        """
        super().__init__(successor)
        self.provider_name = provider_name.lower() # Used for constructing secret name env var
        logger.debug(f"AzureKeyVaultAPIKeyHandler initialized for provider: {self.provider_name}")

    def _get_secret_name_env_var(self) -> str:
        """Constructs the environment variable name that holds the secret name for the provider."""
        # e.g., AZURE_OPENAI_SECRET_NAME, AZURE_ANTHROPIC_SECRET_NAME
        return f"AZURE_{self.provider_name.upper()}_SECRET_NAME"

    def handle(self, provider_name: str) -> Optional[str]:
        """
        Handle the request to retrieve an API key from Azure Key Vault.
        If not found, delegate to the successor in the chain.

        The Key Vault URL is expected in the `AZURE_KEY_VAULT_URL` environment variable.
        The name of the secret (within Key Vault) that stores the API key is expected
        in a provider-specific environment variable (e.g., `AZURE_OPENAI_SECRET_NAME`).

        Args:
            provider_name (str): The name of the AI provider (e.g., "openai", "anthropic").

        Returns:
            Optional[str]: The API key if found, otherwise None.
        """
        key_vault_url = os.environ.get("AZURE_KEY_VAULT_URL")
        secret_name_env_var = self._get_secret_name_env_var()
        secret_name = os.environ.get(secret_name_env_var)

        if not key_vault_url:
            logger.debug("Azure Key Vault URL (AZURE_KEY_VAULT_URL) not set in environment. Skipping Azure Key Vault.")
            if self._successor:
                return self._successor.handle(provider_name)
            return None
        
        if not secret_name:
            logger.debug(
                f"Environment variable for Azure secret name ({secret_name_env_var}) not set for provider {self.provider_name}. "
                "Skipping Azure Key Vault."
            )
            if self._successor:
                return self._successor.handle(provider_name)
            return None

        logger.info(
            f"Attempting to retrieve API key for {self.provider_name} from Azure Key Vault: "
            f"URL='{key_vault_url}', Secret='{secret_name}'"
        )

        try:
            credential = DefaultAzureCredential()
            # Test credential availability early
            try:
                token = credential.get_token("https://vault.azure.net/.default")
                if not token:
                    raise CredentialUnavailableError("Failed to acquire token, no credential available.")
                logger.debug("Azure credential acquired successfully.")
            except CredentialUnavailableError as e:
                logger.warning(f"Azure credential unavailable: {e}. Skipping Azure Key Vault.")
                if self._successor:
                    return self._successor.handle(provider_name)
                return None
            except Exception as e: # Catch other potential errors from get_token
                logger.warning(f"Error testing Azure credential: {e}. Skipping Azure Key Vault.")
                if self._successor:
                    return self._successor.handle(provider_name)
                return None


            secret_client = SecretClient(vault_url=key_vault_url, credential=credential)
            retrieved_secret = secret_client.get_secret(secret_name)
            
            if retrieved_secret and retrieved_secret.value:
                logger.info(
                    f"API key for {self.provider_name} retrieved successfully from Azure Key Vault (secret: {secret_name})."
                )
                return retrieved_secret.value
            else:
                # This case might be rare if get_secret raises an exception for not found or empty value.
                logger.warning(
                    f"API key for {self.provider_name} not found or is empty in Azure Key Vault (secret: {secret_name})."
                )
                if self._successor:
                    return self._successor.handle(provider_name)
                return None

        except ResourceNotFoundError:
            logger.warning(
                f"Secret '{secret_name}' not found in Azure Key Vault '{key_vault_url}' for provider {self.provider_name}."
            )
            if self._successor:
                return self._successor.handle(provider_name)
            return None
        except CredentialUnavailableError as e: # Should be caught by early test, but as a safeguard
            logger.warning(f"Azure credential unavailable during SecretClient operation: {e}. Cannot access Azure Key Vault.")
            if self._successor:
                return self._successor.handle(provider_name)
            return None
        except Exception as e:
            # Catch any other exceptions from Azure SDK or other issues
            logger.error(
                f"An error occurred while trying to retrieve secret '{secret_name}' "
                f"from Azure Key Vault for provider {self.provider_name}: {e}",
                exc_info=True # Log stack trace for unexpected errors
            )
            if self._successor:
                return self._successor.handle(provider_name)
            return None
