import threading
from openai import OpenAI
from groq import Groq
from docu_gen.examples import python
from .env_apikey_handler import EnvAPIKeyHandler
from .azurekeyvault_apikey_handler import AzureKeyVaultAPIKeyHandler
import sys
import os
from docu_gen.core.constant import INFERENCE_CLIENT
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.CRITICAL)


class LLM:
    """A class that represents a Language Model (LLM) supporting multiple providers with
    streaming capabilities."""

    def __init__(self, stream=True):
        """Initialize a Model object with the specified model name and model family.

        Args:
            model_name (str): The name of the model. Defaults to value from AI_MODEL.
            model_family (str): The family to which the model belongs. Defaults to value from AI_MODEL.
            stream (bool): Whether to enable response streaming. Defaults to True.

        Returns:
            None

        Raises:
            ValueError: If the specified model family is not supported.
        """
        self.stream = stream
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the LLM client based on the specified model family.

        Returns:
            None

        Raises:
            ValueError: If the model family is not supported or API key retrieval fails.
        """
        handler_chain = EnvAPIKeyHandler(successor=AzureKeyVaultAPIKeyHandler())
        d = handler_chain.handle()
        api_key = d.get("api_key") if d else None
        inference_client = d.get("inference_client") if d else None
        self.model_name = d.get("model_name") if d else None

        if not api_key:
            logging.error(
                f"Failed to retrieve the {inference_client.upper()} API key from any source.",
            )
            sys.exit(1)

        # Initialize appropriate client
        if inference_client == "openai":
            self.client = OpenAI(api_key=api_key)
        elif inference_client == "groq":
            self.client = Groq(api_key=api_key)
        else:
            raise ValueError(
                f"Inference Client: {inference_client} not supported. Allowed values: {INFERENCE_CLIENT}"
            )

    def _process_streaming_response(self, response):
        """Process streaming response from the LLM.

        Args:
            response: The streaming response object from the LLM.

        Returns:
            str: The complete generated docstring.
        """
        collected_content = []
        for chunk in response:
            if chunk.choices[0].finish_reason is None:
                # Get the content from the chunk
                content = chunk.choices[0].delta.content
                if content is not None:
                    collected_content.append(content)
                    # Optional: Print the chunk as it comes in
                    # logging.info(content, end='', flush=True)

        return "".join(collected_content)

    def generate_docstring(self, code_snippet, code_type):
        """Perform generation of a docstring based on the provided code snippet and
        type.

        Args:
            code_snippet (str): The code snippet for which the docstring needs to be generated.
            code_type (str): The type of code snippet, either "class" or "function".

        Returns:
            str: The generated docstring for the code snippet.

        Raises:
            Exception: If an error occurs during the docstring generation process.
        """
        if code_type == "class":
            examples = python.CLASS_EXAMPLE
            system_message = (
                "You are an expert Python developer. Write clear and concise class-level docstrings "
                "that include only the description of the class, following PEP 257 conventions. "
                "**Do not include any attributes or methods in the docstring.** "
                "Focus on summarizing what the class represents or does."
            )
            user_message = (
                f"Here is an example of a class with its docstring:\n{examples}\n\n"
                f"Now, please generate a docstring for the following class, including only the description. "
                f"Do not include any attributes or methods. "
                f"Do not include the class signature in the docstring.\n\n{code_snippet}\n\nDocstring:"
            )
        else:
            examples = python.FUNCTION_EXAMPLE
            system_message = (
                "You are an expert Python developer. Write clear and comprehensive docstrings "
                "in the Google style guide format, including descriptions of parameters, "
                "return values, and any exceptions raised. "
                "Do not include the function signature in the docstring. "
            )
            user_message = (
                f"Here is an example of a function with its docstring:\n{examples}\n\n"
                f"Now, please generate a docstring for the following code, including parameter "
                f"descriptions, return types, and any raises clauses. "
                f"Do not include the function signature in the docstring. "
                f"Ensure the docstring adheres to PEP 257 conventions.\n\n{code_snippet}\n\nDocstring:"
            )

        messages = [
            {
                "role": "system",
                "content": system_message,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ]

        try:
            # Create completion with streaming enabled
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=1000,
                temperature=0,
                stream=self.stream,
            )

            # Process the response based on streaming mode
            if self.stream:
                docstring = self._process_streaming_response(response)
            else:
                docstring = response.choices[0].message.content.strip()

            # Post-process the docstring
            lines = docstring.split("\n")
            filtered_lines = [
                line
                for line in lines
                if not line.strip().startswith(("def ", "class "))
            ]
            docstring = "\n".join(filtered_lines).strip()
            docstring = docstring.strip('"').strip("'")
            return docstring

        except Exception as e:
            logging.error(f"Error generating docstring: {e}")
            return "Unable to generate docstring."
