from .apikey_handler import APIKeyHandler
import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


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
            secret_name = os.getenv("AZURE_SECRET_NAME")
            if not vault_url or not secret_name:
                raise ValueError("Azure Key Vault URL or Secret Name not set.")

            credential = DefaultAzureCredential()
            client = SecretClient(vault_url=vault_url, credential=credential)
            api_key = client.get_secret(secret_name).value
            if api_key:
                print("API key retrieved from Azure Key Vault.")
                return api_key
            else:
                raise Exception("API key not found in Azure Key Vault.")
        except Exception as e:
            print(f"Azure Key Vault handler error: {e}")
            if self._successor:
                return self._successor.handle()
            else:
                return None
