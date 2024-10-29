from openai import OpenAI
from docu_gen.examples import python
from .env_apikey_handler import EnvAPIKeyHandler
from .azurekeyvault_apikey_handler import AzureKeyVaultAPIKeyHandler
import sys
from docu_gen.core.constant import AI_MODEL


class LLM:
    """A class that represents a Language Model (LLM)."""

    # TODO: allow user to specify model_name and model_family
    def __init__(
        self,
        model_name=AI_MODEL.get("model_name"),
        model_family=AI_MODEL.get("model_family"),
    ):
        """Initialize a Model object with the specified model name and model family.

        Args:
            model_name (str): The name of the model. Defaults to "gpt-3.5-turbo".
            model_family (str): The family to which the model belongs. Defaults to "openai".

        Returns:
            None

        Raises:
            None
        """
        self.model_name = model_name
        self.model_family = model_family

    def initialize_client(self):
        """Initialize the GPT client.

        Returns:
            None

        Raises:
            ValueError: If the model family is not supported.
        """
        handler_chain = EnvAPIKeyHandler(successor=AzureKeyVaultAPIKeyHandler())

        api_key = handler_chain.handle()
        if not api_key:
            print(
                "Failed to retrieve the OpenAI API key from any source.",
                file=sys.stderr,
            )
            sys.exit(1)
        if self.model_family == "openai":
            self.client = OpenAI(
                api_key=api_key,
            )
        else:
            raise ValueError("Model family not supported. Allowed values: ['openai']")

    def generate_docstring(self, code_snippet, code_type):
        """Perform generation of a docstring based on the provided code snippet and
        type.

        Args:
            self: The object instance.
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
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=1000,
                temperature=0,
            )
            docstring = response.choices[0].message.content.strip()
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
            print(f"Error generating docstring: {e}")
            return "Unable to generate docstring."
