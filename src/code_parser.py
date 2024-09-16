import ast
from typing import List, Dict

class CodeParser(ast.NodeVisitor):
    def __init__(self):
        self.functions: List[Dict] = []
        self.classes: List[Dict] = []
        self.imports: List[Dict] = []

    def visit_FunctionDef(self, node):
        """Extract information from a function definition."""
        func_info = {
            'name': node.name,
            'parameters': self.get_parameters_with_defaults(node),
            'return_type': self.get_return_annotation(node),
            'docstring': ast.get_docstring(node),
            'raises': self.get_exceptions(node),
            'constants': self.get_constants(node)
        }
        self.functions.append(func_info)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        """Extract information from a class definition."""
        class_info = {
            'name': node.name,
            'docstring': ast.get_docstring(node),
            'methods': [],
            'constants': self.get_constants(node)
        }

        # Visit class methods
        for elem in node.body:
            if isinstance(elem, ast.FunctionDef):
                method_info = {
                    'name': elem.name,
                    'parameters': self.get_parameters_with_defaults(elem),
                    'return_type': self.get_return_annotation(elem),
                    'docstring': ast.get_docstring(elem),
                    'raises': self.get_exceptions(elem),
                    'constants': self.get_constants(elem)
                }
                class_info['methods'].append(method_info)

        self.classes.append(class_info)
        self.generic_visit(node)

    def visit_Import(self, node):
        """Capture standard imports."""
        for alias in node.names:
            self.imports.append({
                'module': alias.name,
                'alias': alias.asname if alias.asname else alias.name
            })

    def visit_ImportFrom(self, node):
        """Capture from X import Y imports."""
        for alias in node.names:
            self.imports.append({
                'module': f"{node.module}.{alias.name}" if node.module else alias.name,
                'alias': alias.asname if alias.asname else alias.name
            })

    def get_parameters_with_defaults(self, node):
        """Retrieve parameters, their types, and ensure defaults if necessary."""
        parameters = []
        for i, arg in enumerate(node.args.args):
            param_name = arg.arg
            param_type = ast.unparse(arg.annotation) if arg.annotation else None
            param_default = self.get_default_value(node, i, param_type)
            parameters.append({'name': param_name, 'type': param_type, 'default': param_default})
        return parameters

    def get_default_value(self, node, index, param_type):
        """Determine if the parameter has a default value, otherwise assign a default based on type."""
        # Check if there are default values for parameters
        defaults = node.args.defaults
        total_args = len(node.args.args)

        # The default values list aligns from the end, so adjust index accordingly
        if index >= total_args - len(defaults):
            return ast.unparse(defaults[index - (total_args - len(defaults))])

        # Assign default values based on type annotation if no default is provided
        return self.get_type_based_default(param_type)

    def get_type_based_default(self, param_type):
        """Assign default values based on the parameter's type."""
        if param_type == 'int':
            return '0'
        elif param_type == 'float':
            return '0.0'
        elif param_type == 'str':
            return '""'
        elif param_type == 'bool':
            return 'False'
        elif param_type and param_type.startswith('List'):
            return '[]'
        elif param_type and param_type.startswith('Optional'):
            return 'None'
        else:
            return 'None'  # Default to None if type is not clear or specified

    def get_return_annotation(self, node):
        """Retrieve return type annotation if available."""
        if node.returns:
            return ast.unparse(node.returns)  # Python 3.9+ compatibility
        return None

    def get_exceptions(self, node):
        """Retrieve any exceptions that might be raised or handled in the function/method."""
        exceptions = []
        for body_item in ast.walk(node):
            if isinstance(body_item, ast.Raise):
                if body_item.exc:
                    exceptions.append(f"Raises: {ast.unparse(body_item.exc)}")
                else:
                    exceptions.append("Raises: Generic Exception")
            elif isinstance(body_item, ast.Try):
                for handler in body_item.handlers:
                    if handler.type:
                        exceptions.append(f"Catches: {ast.unparse(handler.type)}")
                    else:
                        exceptions.append("Catches: Generic Exception")

                if body_item.finalbody:
                    exceptions.append("Finally: Executes after try/except blocks.")
                if body_item.orelse:
                    exceptions.append("Else: Executes if no exception occurs.")
        return exceptions

    def get_constants(self, node):
        """Retrieve constants within the class, method, or function (Uppercase variables)."""
        constants = []
        for body_item in ast.walk(node):
            if isinstance(body_item, ast.Assign):
                for target in body_item.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():  # Constants are usually uppercase
                        constants.append(f"{target.id}: {ast.unparse(body_item.value)}")
        return constants

    def parse(self, code: str):
        """Parse the given Python code."""
        tree = ast.parse(code)
        self.visit(tree)

    def get_parsed_info(self):
        """Return the extracted functions, classes, and imports information."""
        return {
            'functions': self.functions,
            'classes': self.classes,
            'imports': self.imports
        }

# Function to load and parse Python code
def parse_python_code(code: str):
    parser = CodeParser()
    parser.parse(code)
    return parser.get_parsed_info()

# Example Python code to parse
example_code = """
from typing import List, Optional

class SampleClass:
    CONSTANT_VALUE = 42

    def __init__(self, x: int, y: int = 5):
        self.x = x
        self.y = y

    def divide(self, z: float = 1.0) -> float:
        try:
            return self.x / z
        except ZeroDivisionError:
            raise ValueError("Cannot divide by zero")

def sample_function(a: int, b: int = 0) -> int:
    return a + b

def function_without_defaults(x: int, y: Optional[str]) -> None:
    pass
"""

# Parse the code
parsed_info = parse_python_code(example_code)

# Print parsed information
import pprint
pprint.pprint(parsed_info)
