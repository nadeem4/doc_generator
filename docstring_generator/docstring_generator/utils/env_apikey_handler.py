from .apikey_handler import APIKeyHandler
import os


# Handler for environment variables
class EnvAPIKeyHandler(APIKeyHandler):
    def handle(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            print("API key retrieved from environment variable.")
            return api_key
        elif self._successor:
            return self._successor.handle()
        else:
            return None
