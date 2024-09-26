import ast
import astor
import docformatter.format
from openai import OpenAI
import os
import tempfile
import docformatter
import pydocstyle

# Set your OpenAI API key
client = OpenAI(
    # This is the default and can be omitted
    api_key='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',
)


def generate_docstring(code_snippet, code_type):
    """
    Generate a detailed docstring for the given code snippet using OpenAI's API.
    """
    # Examples for few-shot learning
    if code_type == 'class':
        examples = '''
                class ExampleClass:
                    """
                    A class that represents an example.
                    """
                '''
        # Prepare the messages for the ChatCompletion API
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
        examples = '''
        def example_function(param1, param2):
            """
            Perform an example operation.

            Args:
                param1 (int): The first parameter.
                param2 (int): The second parameter.

            Returns:
                int: The result of the operation.

            Raises:
                ValueError: If invalid parameters are provided.
            """
            if param1 < 0 or param2 < 0:
                raise ValueError("Parameters must be non-negative.")
            return param1 + param2
        '''
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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use 'gpt-4' if you have access
            messages=messages,
            max_tokens=1000,
            temperature=0,
        )
        docstring = response.choices[0].message.content.strip()
        # Remove any function signatures from the docstring if present
        lines = docstring.split('\n')
        filtered_lines = [line for line in lines if not line.strip().startswith(('def ', 'class '))]
        docstring = '\n'.join(filtered_lines).strip()
        # Remove any surrounding quotes if present
        docstring = docstring.strip('\"').strip("'")
        return docstring
    except Exception as e:
        print(f"Error generating docstring: {e}")
        return ""

def add_docstrings(source_code):
    """
    Add docstrings to functions, methods, and classes without changing any code.
    """
    tree = ast.parse(source_code)

    class DocstringAdder(ast.NodeTransformer):
        def visit_FunctionDef(self, node):
            self.generic_visit(node)

            if ast.get_docstring(node) is None:
                # Check if this is a method (parent is a class) or a function
                if hasattr(node, 'parent') and isinstance(node.parent, ast.ClassDef):
                    # Method
                    node_copy = ast.FunctionDef(
                        name=node.name,
                        args=node.args,
                        body=node.body,
                        decorator_list=[],
                        returns=node.returns,
                        type_comment=node.type_comment,
                    )
                    method_code = astor.to_source(node_copy)
                    # Generate the docstring
                    docstring = generate_docstring(method_code, code_type='method')
                else:
                    # Function
                    node_copy = ast.FunctionDef(
                        name=node.name,
                        args=node.args,
                        body=node.body,
                        decorator_list=[],
                        returns=node.returns,
                        type_comment=node.type_comment,
                    )
                    func_code = astor.to_source(node_copy)
                    # Generate the docstring
                    docstring = generate_docstring(func_code, code_type='function')

                if docstring:
                    # Create a new docstring node
                    new_docstring = ast.Expr(value=ast.Constant(value=docstring))
                    # Insert the docstring at the beginning of the function body
                    node.body.insert(0, new_docstring)
            return node

        def visit_ClassDef(self, node):
            self.generic_visit(node)
            if ast.get_docstring(node) is None:
                # Include the __init__ method and attribute assignments
                init_method = next((n for n in node.body if isinstance(n, ast.FunctionDef) and n.name == '__init__'), None)
                if init_method:
                    # Create a copy of the __init__ method
                    init_method_copy = ast.FunctionDef(
                        name=init_method.name,
                        args=init_method.args,
                        body=init_method.body,
                        decorator_list=[],
                        returns=init_method.returns,
                        type_comment=init_method.type_comment,
                    )
                    # Create a simplified class node
                    node_copy = ast.ClassDef(
                        name=node.name,
                        bases=[],
                        keywords=[],
                        body=[init_method_copy],
                        decorator_list=[],
                    )
                else:
                    # If no __init__, create an empty class
                    node_copy = ast.ClassDef(
                        name=node.name,
                        bases=[],
                        keywords=[],
                        body=[ast.Pass()],
                        decorator_list=[],
                    )

                class_code = astor.to_source(node_copy)
                # Generate the docstring
                docstring = generate_docstring(class_code, code_type='class')
                if docstring:
                    # Create a new docstring node
                    new_docstring = ast.Expr(value=ast.Constant(value=docstring))
                    # Insert the docstring at the beginning of the class body
                    node.body.insert(0, new_docstring)
            return node

    # Set parent references in the AST nodes
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node

    transformer = DocstringAdder()
    new_tree = transformer.visit(tree)
    # Convert the AST back to source code
    new_source_code = astor.to_source(new_tree)

    return new_source_code


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python add_docstrings.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        source_code = f.read()
    new_code = add_docstrings(source_code)
    with open('output_with_docstrings.py', 'w') as f:
        f.write(new_code)
    print("Docstrings added and formatted successfully. Check 'output_with_docstrings.py'.")
