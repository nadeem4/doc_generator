import os
import fnmatch
import libcst as cst
from doc_craft.utils.llm import LLM
from doc_craft.core.validate import validate_only_docstrings_added


class DocstringAdder(cst.CSTTransformer):
    """A class that adds docstrings to other classes."""

    def __init__(self, override=False):
        """Initialize the object with optional override flag.

        Args:
            override (bool, optional): A flag indicating whether to override certain settings. Defaults to False.

        Raises:
            None

        Returns:
            None
        """
        super().__init__()
        self.llm = LLM()
        self.llm.initialize_client()
        self.current_class_name = None
        self.override = override

    def visit_ClassDef(self, node):
        """Update the current class name when entering a class definition.

        Args:
            node (ast.ClassDef): The AST node representing the class definition.

        Returns:
            None

        Raises:
            None
        """
        # Entering a class definition
        self.current_class_name = node.name.value

    def leave_ClassDef(self, original_node, updated_node):
        """Leaves the ClassDef node with an updated docstring.

        Checks if the class already has a docstring. If not, generates a docstring based on the simplified class code for the LLM (Language Model). Inserts the generated docstring at the beginning of the class body.

        Args:
            self: The instance of the class.
            original_node (cst.ClassDef): The original ClassDef node.
            updated_node (cst.ClassDef): The updated ClassDef node.

        Returns:
            cst.ClassDef: The updated ClassDef node with the inserted docstring.

        Raises:
            None.
        """
        if self.override or not self._has_docstring(original_node.body.body):
            class_code = self._get_class_code(original_node)
            docstring = self.llm.generate_docstring(class_code, code_type="class")
            if docstring:
                docstring_node = cst.SimpleStatementLine(
                    body=[cst.Expr(value=cst.SimpleString(f'"""{docstring}"""'))]
                )
                new_body = [docstring_node] + list(
                    updated_node.body.body[1:]
                    if self.override
                    else updated_node.body.body
                )
                updated_node = updated_node.with_changes(
                    body=updated_node.body.with_changes(body=new_body)
                )
        self.current_class_name = None
        return updated_node

    def leave_FunctionDef(self, original_node, updated_node):
        """Check if the function already has a docstring and add one if needed.

        Args:
            self: The instance of the class.
            original_node: The original AST node representing the function definition.
            updated_node: The updated AST node representing the function definition.

        Returns:
            cst.FunctionDef: The updated AST node with the docstring added if necessary.

        Raises:
            N/A
        """
        if self.override or not self._has_docstring(original_node.body.body):
            function_code = self._get_code_without_decorators(original_node)
            is_method = self.current_class_name is not None
            code_type = "method" if is_method else "function"
            docstring = self.llm.generate_docstring(function_code, code_type=code_type)
            if docstring:
                docstring_node = cst.SimpleStatementLine(
                    body=[cst.Expr(value=cst.SimpleString(f'"""{docstring}"""'))]
                )
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
        """Check if a given body has a docstring.

        Args:
            self: The object instance.
            body (List[cst.BaseStatement]): The body of the function or class to check for a docstring.

        Returns:
            bool: True if the body contains a docstring, False otherwise.

        Raises:
            None.
        """
        if body and isinstance(body[0], cst.SimpleStatementLine):
            stmt = body[0].body[0]
            if isinstance(stmt, cst.Expr) and isinstance(stmt.value, cst.SimpleString):
                return True
        return False

    def _get_code_without_decorators(self, node):
        """Get the code of a function without decorators.

        Args:
            self: The instance of the class.
            node (cst.FunctionDef): The function node containing decorators.

        Returns:
            str: The code of the function without decorators.

        Raises:
            None.
        """
        function_def = node.with_changes(decorators=[])
        module = cst.Module(body=[function_def])
        function_code = module.code
        return function_code

    def _get_class_code(self, node):
        """Extracts the code for a class containing only the __init__ method and
        attribute assignments.

        Args:
            self: The instance of the class.
            node (cst.ClassDef): The class node to extract code from.

        Returns:
            str: The code representing the class with only the __init__ method and attribute assignments.

        Raises:
            None.
        """
        init_method = None
        for element in node.body.body:
            if (
                isinstance(element, cst.FunctionDef)
                and element.name.value == "__init__"
            ):
                init_method = element.with_changes(decorators=[])
                break
        if init_method:
            class_def = node.with_changes(
                bases=[], decorators=[], body=node.body.with_changes(body=[init_method])
            )
        else:
            pass_stmt = cst.SimpleStatementLine(body=[cst.Pass()])
            class_def = node.with_changes(
                bases=[], decorators=[], body=node.body.with_changes(body=[pass_stmt])
            )
        module = cst.Module(body=[class_def])
        class_code = module.code
        return class_code


class ClassOrFunctionFinder(cst.CSTVisitor):
    """A class that identifies the presence of classes or functions within a
    codebase."""

    def __init__(self):
        """Initialize the object with a default value for the 'has_class_or_function'
        attribute.

        Attributes:
            self.has_class_or_function (bool): A boolean flag indicating if the object has a class or function.

        Raises:
            None
        """
        self.has_class_or_function = False

    def visit_ClassDef(self, node):
        """Updates a flag to indicate the presence of a class or function in the AST
        node.

        Args:
            self: The object instance.
            node: The AST node representing a class definition.

        Returns:
            bool: False to stop traversal since a class is found.

        Raises:
            None.
        """
        self.has_class_or_function = True
        return False

    def visit_FunctionDef(self, node):
        """Visit a FunctionDef node in an abstract syntax tree (AST).

        This method is called when traversing an AST node representing a function definition.

        Args:
            self: The object instance.
            node: ast.FunctionDef - The AST node representing a function definition.

        Returns:
            bool: False to stop traversal since a function node has been found.

        Raises:
            None.
        """
        self.has_class_or_function = True
        return False


def add_docstrings_to_code(source_code, file_path, override=False):
    """Add docstrings to classes and functions in Python source code.

    Args:
        source_code (str): The source code to analyze and add docstrings to.
        file_path (str): The path to the file containing the source code.
        override (bool, optional): Whether to override existing docstrings. Defaults to False.

    Returns:
        str: The modified source code with added docstrings.

    Raises:
        None
    """
    module = cst.parse_module(source_code)

    if not any(
        not isinstance(stmt, (cst.EmptyLine, cst.SimpleStatementLine))
        or (
            isinstance(stmt, cst.SimpleStatementLine)
            and not isinstance(stmt.body[0], cst.Expr)
        )
        for stmt in module.body
    ):
        print(
            f"File '{file_path}' is empty or contains only comments and will be skipped."
        )
        return source_code

    class_or_function_finder = ClassOrFunctionFinder()
    module.visit(class_or_function_finder)

    if not class_or_function_finder.has_class_or_function:
        print(
            f"File '{file_path}' does not contain classes, methods, or functions and will be skipped."
        )
        return source_code

    transformer = DocstringAdder(override=override)
    modified_tree = module.visit(transformer)
    return modified_tree.code


def add_docstrings_to_file(file_path, override=False):
    """Add docstrings to the functions in a Python file and write them back to the file.

    Args:
        file_path (str): The path to the Python file to process.
        override (bool, optional): Whether to override existing docstrings. Defaults to False.

    Raises:
        FileNotFoundError: If the specified file_path does not exist.
        PermissionError: If the file cannot be opened due to permission issues.
        UnicodeDecodeError: If the file cannot be decoded using the specified encoding.
        IOError: If an I/O error occurs while reading or writing the file.
    """
    print(f"Processing file: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    if not source_code.strip():
        print(f"File '{file_path}' is empty and will be skipped.")
        return

    modified_code = add_docstrings_to_code(source_code, file_path, override)

    print(f"Validating changes for file: {file_path}")
    if validate_only_docstrings_added(source_code, modified_code):
        if modified_code != source_code:
            print(f"Generated Docstring for: {file_path}")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(modified_code)
                print(f"Validation passed for file: {file_path}. Changes written.")
        else:
            print(f"No changes made to file: {file_path}")
    else:
        print(
            f"Validation failed for file '{file_path}'. Code was modified beyond adding docstrings."
        )


def is_excluded(file_path, exclude_patterns):
    """Check if a file path is excluded based on a list of patterns.

    Args:
        file_path (str): The file path to check for exclusion.
        exclude_patterns (list): A list of patterns to match against the file path.

    Returns:
        bool: True if the file path is excluded by any of the patterns, False otherwise.

    Raises:
        None
    """
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(os.path.abspath(file_path), os.path.abspath(pattern)):
            return True
    return False
