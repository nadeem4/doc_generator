from .apikey_handler import APIKeyHandler
import os


# Handler for environment variables
class EnvAPIKeyHandler(APIKeyHandler):
    """A class that serves as a handler for environment variables."""

    def handle(self):
        """Retrieve the OpenAI API key.

        Returns:
            str: The OpenAI API key if retrieved successfully, otherwise None.

        Raises:
            None.
        """
        api_key = os.getenv("API_KEY")
        inference_client = os.getenv("INFERENCE_CLIENT")
        model_name = os.getenv("MODEL_NAME")

        if api_key and inference_client and model_name:
            return {
                "api_key": api_key,
                "inference_client": inference_client,
                "model_name": model_name,
            }
        elif self._successor:
            return self._successor.handle()
        else:
            return None
