import os
import sys
import argparse
import fnmatch
import libcst as cst
from docstring_generator.utils.llm import LLM


class DocstringAdder(cst.CSTTransformer):
    def __init__(self, override=False):
        super().__init__()
        self.llm = LLM()
        self.llm.initialize_client()
        self.current_class_name = None  # Track the current class context
        self.override = override

    def visit_ClassDef(self, node):
        # Entering a class definition
        self.current_class_name = node.name.value

    def leave_ClassDef(self, original_node, updated_node):
        # Check if the class already has a docstring
        if self.override or not self._has_docstring(original_node.body.body):
            # Get simplified class code for the LLM
            class_code = self._get_class_code(original_node)
            # Generate the docstring
            docstring = self.llm.generate_docstring(class_code, code_type="class")
            if docstring:
                # Create a new docstring node
                docstring_node = cst.SimpleStatementLine(
                    body=[cst.Expr(value=cst.SimpleString(f'"""{docstring}"""'))]
                )
                # Insert the docstring at the beginning of the class body
                new_body = [docstring_node] + list(
                    updated_node.body.body[1:]
                    if self.override
                    else updated_node.body.body
                )
                updated_node = updated_node.with_changes(
                    body=updated_node.body.with_changes(body=new_body)
                )
        # Exiting the class definition
        self.current_class_name = None
        return updated_node

    def leave_FunctionDef(self, original_node, updated_node):
        # Check if the function already has a docstring
        if self.override or not self._has_docstring(original_node.body.body):
            # Remove decorators when generating code for the LLM
            function_code = self._get_code_without_decorators(original_node)
            # Determine if the function is a method
            is_method = self.current_class_name is not None
            code_type = "method" if is_method else "function"
            # Generate the docstring
            docstring = self.llm.generate_docstring(function_code, code_type=code_type)
            if docstring:
                # Create a new docstring node
                docstring_node = cst.SimpleStatementLine(
                    body=[cst.Expr(value=cst.SimpleString(f'"""{docstring}"""'))]
                )
                # Insert the docstring at the beginning of the function body
                new_body = [docstring_node] + list(
                    updated_node.body.body[1:]
                    if self.override
                    else updated_node.body.body
                )
                updated_node = updated_node.with_changes(
                    body=updated_node.body.with_changes(body=new_body)
                )
        return updated_node

    def _has_docstring(self, body):
        if body and isinstance(body[0], cst.SimpleStatementLine):
            stmt = body[0].body[0]
            if isinstance(stmt, cst.Expr) and isinstance(stmt.value, cst.SimpleString):
                return True
        return False

    def _get_code_without_decorators(self, node):
        # Create a copy of the function without decorators
        function_def = node.with_changes(decorators=[])
        # Generate code from the function definition
        module = cst.Module(body=[function_def])
        function_code = module.code
        return function_code

    def _get_class_code(self, node):
        # Include only the __init__ method and attribute assignments
        init_method = None
        for element in node.body.body:
            if (
                isinstance(element, cst.FunctionDef)
                and element.name.value == "__init__"
            ):
                init_method = element.with_changes(decorators=[])
                break
        if init_method:
            # Create a simplified class node with the __init__ method
            class_def = node.with_changes(
                bases=[], decorators=[], body=node.body.with_changes(body=[init_method])
            )
        else:
            # Create an empty class if no __init__ method
            pass_stmt = cst.SimpleStatementLine(body=[cst.Pass()])
            class_def = node.with_changes(
                bases=[], decorators=[], body=node.body.with_changes(body=[pass_stmt])
            )
        # Generate code from the class definition
        module = cst.Module(body=[class_def])
        class_code = module.code
        return class_code


class ClassOrFunctionFinder(cst.CSTVisitor):
    def __init__(self):
        self.has_class_or_function = False

    def visit_ClassDef(self, node):
        self.has_class_or_function = True
        return False  # Stop traversal since we found a class

    def visit_FunctionDef(self, node):
        self.has_class_or_function = True
        return False  # Stop traversal since we found a function


def add_docstrings_to_code(source_code, file_path, override=False):
    module = cst.parse_module(source_code)

    # Check if the module is empty or contains only comments and whitespace
    if not any(
        not isinstance(stmt, (cst.EmptyLine, cst.SimpleStatementLine))
        or (
            isinstance(stmt, cst.SimpleStatementLine)
            and not isinstance(stmt.body[0], cst.Expr)
        )
        for stmt in module.body
    ):
        # File is empty or contains only comments
        print(
            f"File '{file_path}' is empty or contains only comments and will be skipped."
        )
        return source_code

    # Find if the module contains any classes or functions
    class_or_function_finder = ClassOrFunctionFinder()
    module.visit(class_or_function_finder)

    if not class_or_function_finder.has_class_or_function:
        # Skip transformation if the module doesn't contain classes or functions
        print(
            f"File '{file_path}' does not contain classes, methods, or functions and will be skipped."
        )
        return source_code

    transformer = DocstringAdder(override=override)
    modified_tree = module.visit(transformer)
    return modified_tree.code


def add_docstrings_to_file(file_path, override=False):
    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    # Check if the file is empty
    if not source_code.strip():
        # Skip processing empty files
        print(f"File '{file_path}' is empty and will be skipped.")
        return

    modified_code = add_docstrings_to_code(source_code, file_path, override)

    # Only write back if changes were made
    if modified_code != source_code:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(modified_code)
    else:
        # If no changes were made, you can print a message if desired
        pass


def is_excluded(file_path, exclude_patterns):
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(os.path.abspath(file_path), os.path.abspath(pattern)):
            return True
    return False
