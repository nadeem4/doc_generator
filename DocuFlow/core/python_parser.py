# my_project/core/parser.py
import ast
from typing import List, Dict

class PythonParser(ast.NodeVisitor):
    def __init__(self):
        self.functions: List[Dict] = []
        self.classes: List[Dict] = []
        self.imports: List[Dict] = []

    def visit_FunctionDef(self, node):
        func_info = {
            'name': node.name,
            'definition': ast.unparse(node),
            'parameters': self.get_parameters_with_defaults(node),
            'return_type': self.get_return_annotation(node),
            'docstring': ast.get_docstring(node),
            'raises': self.get_exceptions(node),
            'constants': self.get_constants(node)
        }
        self.functions.append(func_info)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        class_info = {
            'name': node.name,
            'definition': ast.unparse(node),
            'docstring': ast.get_docstring(node),
            'methods': [],
            'constants': self.get_constants(node)
        }
        for elem in node.body:
            if isinstance(elem, ast.FunctionDef):
                method_info = {
                    'name': elem.name,
                    'definition': ast.unparse(elem),
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
        for alias in node.names:
            self.imports.append({
                'module': alias.name,
                'alias': alias.asname if alias.asname else alias.name
            })

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imports.append({
                'module': f"{node.module}.{alias.name}" if node.module else alias.name,
                'alias': alias.asname if alias.asname else alias.name
            })

    def get_parameters_with_defaults(self, node):
        parameters = []
        for i, arg in enumerate(node.args.args):
            param_name = arg.arg
            param_type = ast.unparse(arg.annotation) if arg.annotation else None
            param_default = self.get_default_value(node, i, param_type)
            parameters.append({'name': param_name, 'type': param_type, 'default': param_default})
        return parameters

    def get_default_value(self, node, index, param_type):
        defaults = node.args.defaults
        total_args = len(node.args.args)
        if index >= total_args - len(defaults):
            return ast.unparse(defaults[index - (total_args - len(defaults))])
        return self.get_type_based_default(param_type)

    def get_type_based_default(self, param_type):
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
            return 'None'

    def get_return_annotation(self, node):
        if node.returns:
            return ast.unparse(node.returns)
        return None

    def get_exceptions(self, node):
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
        constants = []
        for body_item in ast.walk(node):
            if isinstance(body_item, ast.Assign):
                for target in body_item.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        constants.append(f"{target.id}: {ast.unparse(body_item.value)}")
        return constants

    def parse(self, code: str):
        tree = ast.parse(code)
        self.visit(tree)

    def get_parsed_info(self):
        return {
            'functions': self.functions,
            'classes': self.classes,
            'imports': self.imports
        }
