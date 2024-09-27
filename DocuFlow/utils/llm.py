from openai import OpenAI
from examples import python


class LLM:
    # default the model name to gpt 3.5 turbo
    def __init__(self, model_name="gpt-3.5-turbo", model_family="openai"):
        self.model_name = model_name
        self.model_family = model_family

    # initialize the gpt client
    def initialize_client(self):
        # initialize the client
        if self.model_family == "openai":
            self.client = OpenAI(
                # This is the default and can be omitted
                api_key="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",
            )
        else:
            raise ValueError("Model family not supported. Allowed values: ['openai']")

    def generate_docstring(self, code_snippet, code_type):
        # Examples for few-shot learning
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
            # Prepare the messages for the ChatCompletion API
            system_message = (
                "You are an expert Python developer. Write clear and comprehensive docstrings "
                "in the Google style guide format, including descriptions of parameters, "
                "return values, and any exceptions raised. "
                "Do not include the function signature in the docstring. "
                "Ensure the docstring adheres to PEP 257 conventions."
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
            # Remove any function signatures from the docstring if present
            lines = docstring.split("\n")
            filtered_lines = [
                line
                for line in lines
                if not line.strip().startswith(("def ", "class "))
            ]
            docstring = "\n".join(filtered_lines).strip()
            # Remove any surrounding quotes if present
            docstring = docstring.strip('"').strip("'")
            return docstring
        except Exception as e:
            print(f"Error generating docstring: {e}")
            return "Unable to generate docstring."
