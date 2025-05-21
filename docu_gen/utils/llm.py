import os
import sys
import logging # Import logging
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_cohere import ChatCohere
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from docu_gen.utils.apikey_handler import APIKeyHandler
from docu_gen.utils.cli_apikey_handler import CLIAPIKeyHandler
from docu_gen.utils.env_apikey_handler import EnvAPIKeyHandler
from docu_gen.utils.azurekeyvault_apikey_handler import AzureKeyVaultAPIKeyHandler

# from docu_gen.core.constant import AI_MODEL # Only if used for default model name

# Get a logger instance for this module
logger = logging.getLogger("docu_gen")

class LLM:
    """A class to interact with Large Language Models using Langchain."""

    def __init__(self, provider: str = "openai", model_name: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initializes the LLM class with a specific provider, model name, and optional API key.

        Args:
            provider (str): The name of the LLM provider (e.g., "openai", "anthropic", "cohere", "ollama").
            model_name (Optional[str]): The specific model name for the provider.
                                       If None, a default model might be used by the provider's client.
            api_key (Optional[str]): An API key to directly initialize the client.
                                     If None, the API key will be resolved using handlers.
        """
        self.provider = provider.lower()
        self.model_name = model_name
        self.api_key = api_key # Store API key if provided directly
        self.client = None
        self.output_parser = StrOutputParser()
        self.prompt_template = self._get_prompt_template()

        # Setup API key handler chain
        self.key_handler = CLIAPIKeyHandler(provider_name=self.provider, api_key=self.api_key) # Pass CLI API key here
        env_handler = EnvAPIKeyHandler(provider_name=self.provider)
        azure_handler = AzureKeyVaultAPIKeyHandler(provider_name=self.provider)
        
        self.key_handler.set_successor(env_handler)
        env_handler.set_successor(azure_handler)
        
        logger.debug(f"LLM initialized for provider: {self.provider}, model: {self.model_name}")

    def _resolve_api_key(self) -> Optional[str]:
        """
        Resolves the API key using the handler chain if not already provided.
        """
        if self.api_key: # API key was provided during __init__
            logger.debug(f"Using API key provided directly for {self.provider}.")
            return self.api_key
        
        resolved_key = self.key_handler.handle(self.provider) # Pass provider name to start chain
        
        if not resolved_key:
            # For Ollama, an API key is typically not required.
            if self.provider == "ollama":
                logger.info("Ollama provider selected, no API key needed.")
                return None # Explicitly return None for Ollama if no key is expected
            logger.warning(f"Failed to retrieve API key for provider: {self.provider} from any source.")
        return resolved_key

    def initialize_client(self) -> None:
        """
        Initializes the Langchain chat client based on the provider and resolved API key.
        Exits if initialization fails for providers requiring an API key.
        """
        if self.client:
            logger.debug(f"Client for {self.provider} already initialized.")
            return

        resolved_api_key = self._resolve_api_key()

        # For providers that require an API key, exit if not found.
        if self.provider not in ["ollama"] and not resolved_api_key:
            logger.error(
                f"API key for {self.provider} is required but could not be resolved. "
                "Please provide it via --api-key, environment variable, or Azure Key Vault."
            )
            sys.exit(1) # Exit if critical API key is missing

        try:
            if self.provider == "openai":
                self.client = ChatOpenAI(model_name=self.model_name or "gpt-3.5-turbo", api_key=resolved_api_key)
            elif self.provider == "anthropic":
                self.client = ChatAnthropic(model_name=self.model_name or "claude-3-haiku-20240307", api_key=resolved_api_key)
            elif self.provider == "cohere":
                self.client = ChatCohere(model_name=self.model_name or "command", api_key=resolved_api_key)
            elif self.provider == "ollama":
                # Ollama typically doesn't use an API key. Base URL can be configured via env var OLLAMA_BASE_URL.
                self.client = ChatOllama(model=self.model_name or "llama3") # Default to llama3 if no model specified
            else:
                logger.error(f"Unsupported LLM provider: {self.provider}")
                sys.exit(1)
            logger.info(f"Successfully initialized LLM client for provider: {self.provider} with model: {self.model_name or 'default'}")
        except Exception as e:
            logger.error(f"Error initializing LLM client for {self.provider} (model: {self.model_name or 'default'}): {e}", exc_info=True)
            sys.exit(1) # Exit on critical initialization failure

    def _get_prompt_template(self):
        """Returns a generic prompt template for docstring generation."""
        # This template can be further customized.
        return ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant that generates Python docstrings. "
                       "Generate a concise and informative docstring for the following Python {code_type}. "
                       "The docstring should follow standard Python conventions (e.g., Google style or reStructuredText). "
                       "Focus on explaining what the {code_type} does, its arguments (if any), and what it returns (if any). "
                       "Do not include the original code in your response, only the docstring content itself. "
                       "If it's a class, describe the class and its purpose. If it's a method or function, describe its operation, parameters, and return values."),
            ("human", "{code_snippet}")
        ])

    def generate_docstring(self, code_snippet: str, code_type: str = "code") -> str:
        """
        Generates a docstring for a given code snippet.

        Args:
            code_snippet (str): The Python code snippet (e.g., function, class, method).
            code_type (str): The type of code ('function', 'class', 'method').

        Returns:
            str: The generated docstring, or an error message if generation fails.
        """
        if not self.client:
            logger.info("LLM client not initialized. Attempting to initialize now...")
            self.initialize_client()
            if not self.client: # Still not initialized after attempt
                logger.error("Failed to initialize LLM client. Cannot generate docstring.")
                return "Unable to generate docstring due to client initialization failure."
        
        chain = self.prompt_template | self.client | self.output_parser
        
        try:
            logger.debug(f"Requesting docstring for {code_type} from provider {self.provider} (model: {self.model_name or 'default'}). Snippet length: {len(code_snippet)}")
            response = chain.invoke({"code_snippet": code_snippet, "code_type": code_type})
            logger.debug(f"LLM response received for {code_type}. Length: {len(response)}")
            # Basic cleaning: remove triple quotes if LLM includes them
            if response.startswith('"""') and response.endswith('"""'):
                response = response[3:-3].strip()
            elif response.startswith("'''") and response.endswith("'''"):
                response = response[3:-3].strip()
            return response.strip()
        except Exception as e:
            logger.error(f"Error generating docstring with provider {self.provider} (model: {self.model_name or 'default'}): {e}", exc_info=True)
            return "Unable to generate docstring."

# Example usage (for testing purposes, not part of the library's main flow)
if __name__ == "__main__":
    from docu_gen.utils.logging_config import setup_logging
    setup_logging(level="DEBUG") # Setup logging for standalone test

    # Test with OpenAI (requires OPENAI_API_KEY to be set in env or passed)
    # os.environ["OPENAI_API_KEY"] = "your_key_here" # Uncomment and set for testing
    logger.info("Testing LLM with OpenAI...")
    llm_openai = LLM(provider="openai", model_name="gpt-3.5-turbo")
    # llm_openai.initialize_client() # Not strictly needed before first generate_docstring call
    code_sample_func = "def example_function(a, b):\n    return a + b"
    docstring_openai = llm_openai.generate_docstring(code_sample_func, "function")
    logger.info(f"OpenAI generated docstring:\n---\n{docstring_openai}\n---")

    # Test with Ollama (requires Ollama server to be running with llama3 model)
    logger.info("Testing LLM with Ollama...")
    llm_ollama = LLM(provider="ollama", model_name="llama3") # or any other model you have
    code_sample_class = "class MySampleClass:\n    def __init__(self, x):\n        self.x = x"
    docstring_ollama = llm_ollama.generate_docstring(code_sample_class, "class")
    logger.info(f"Ollama generated docstring:\n---\n{docstring_ollama}\n---")

    # Test API key resolution failure (example)
    # logger.info("Testing API key resolution failure for a dummy provider...")
    # llm_fail = LLM(provider="dummy_provider_requires_key")
    # llm_fail.initialize_client() # This should log an error and exit
