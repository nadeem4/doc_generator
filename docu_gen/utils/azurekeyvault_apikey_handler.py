from .apikey_handler import APIKeyHandler
import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import logging


# Handler for Azure Key Vault
class AzureKeyVaultAPIKeyHandler(APIKeyHandler):
    """Handler for Azure Key Vault."""

    def handle(self):
        """Retrieve an API key from Azure Key Vault.

        Returns the API key retrieved from Azure Key Vault.

        Raises:
            ValueError: If Azure Key Vault URL or Secret Name are not set.
            Exception: If the API key is not found in Azure Key Vault.
        """
        try:
            vault_url = os.getenv("AZURE_KEY_VAULT_URL")
            apikey_secret_name = os.getenv("API_KEY_SECRET_NAME")
            inference_client = os.getenv("INFERENCE_CLIENT")
            model_name = os.getenv("MODEL_NAME")

            if not vault_url:
                raise ValueError("Azure Key Vault URL is not set.")
            if not apikey_secret_name:
                raise ValueError("API Key Secret Name is not set.")
            if not inference_client:
                raise ValueError("Inference Client is not set.")
            if not model_name:
                raise ValueError("Model Name is not set.")

            credential = DefaultAzureCredential()
            client = SecretClient(vault_url=vault_url, credential=credential)

            api_key = client.get_secret(apikey_secret_name).value

            if api_key:
                return {
                    "api_key": api_key,
                    "inference_client": inference_client,
                    "model_name": model_name,
                }
            else:
                raise Exception("API key not found in Azure Key Vault.")
        except Exception as e:
            logging.error(f"Azure Key Vault handler error: {e}")
            if self._successor:
                return self._successor.handle()
            else:
                return None
