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
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            print("API key retrieved from environment variable.")
            return api_key
        elif self._successor:
            return self._successor.handle()
        else:
            return None
