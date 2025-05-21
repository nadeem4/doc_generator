import os
import fnmatch
import libcst as cst
import logging # Import logging
from docu_gen.utils.llm import LLM
from docu_gen.core.validate import validate_only_docstrings_added

# Get a logger instance for this module
logger = logging.getLogger("docu_gen")

class DocstringAdder(cst.CSTTransformer):
    """A class that adds docstrings to other classes."""

    def __init__(self, override=False, provider="openai", model_name="gpt-3.5-turbo"):
        """Initialize the object with optional override flag, provider, and model name.

        Args:
            override (bool, optional): A flag indicating whether to override certain settings. Defaults to False.
            provider (str, optional): The AI provider to use. Defaults to "openai".
            model_name (str, optional): The model name to use. Defaults to "gpt-3.5-turbo".
        """
        super().__init__()
        logger.debug(f"DocstringAdder initialized with: override={override}, provider='{provider}', model_name='{model_name}'")
        self.llm = LLM(provider=provider, model_name=model_name)
        # self.llm.initialize_client() # Client initialization is now handled within LLM class methods if needed
        self.current_class_name = None
        self.override = override

    def visit_ClassDef(self, node):
        """Update the current class name when entering a class definition.

        Args:
            node (cst.ClassDef): The AST node representing the class definition.
        """
        self.current_class_name = node.name.value
        logger.debug(f"Entering class definition: {self.current_class_name}")

    def leave_ClassDef(self, original_node, updated_node):
        """Leaves the ClassDef node with an updated docstring.

        Checks if the class already has a docstring. If not, or if override is True,
        generates a docstring based on the simplified class code for the LLM.
        Inserts the generated docstring at the beginning of the class body.

        Args:
            original_node (cst.ClassDef): The original ClassDef node.
            updated_node (cst.ClassDef): The updated ClassDef node.

        Returns:
            cst.ClassDef: The updated ClassDef node with the inserted docstring.
        """
        class_name = original_node.name.value
        has_existing_docstring = self._has_docstring(original_node.body.body)
        logger.debug(f"Leaving class: {class_name}, override: {self.override}, has_docstring: {has_existing_docstring}")

        if self.override or not has_existing_docstring:
            class_code = self._get_class_code(original_node)
            if not class_code.strip(): # Avoid sending empty code to LLM
                logger.warning(f"Skipping docstring generation for class '{class_name}' as its parsable code is empty.")
                self.current_class_name = None
                return updated_node

            docstring_text = self.llm.generate_docstring(class_code, code_type="class")
            
            if docstring_text and "Unable to generate docstring" not in docstring_text:
                logger.info(f"Generated docstring for class: {class_name}")
                docstring_node = cst.SimpleStatementLine(
                    body=[cst.Expr(value=cst.SimpleString(f'"""{docstring_text}"""'))]
                )
                
                current_body_elements = list(updated_node.body.body)
                if has_existing_docstring and self.override and current_body_elements and \
                   isinstance(current_body_elements[0], cst.SimpleStatementLine) and \
                   isinstance(current_body_elements[0].body[0], cst.Expr) and \
                   isinstance(current_body_elements[0].body[0].value, cst.SimpleString):
                    # Remove existing docstring before adding new one
                    new_body = [docstring_node] + current_body_elements[1:]
                else:
                    new_body = [docstring_node] + current_body_elements
                
                updated_node = updated_node.with_changes(
                    body=updated_node.body.with_changes(body=new_body)
                )
            elif "Unable to generate docstring" in docstring_text:
                 logger.error(f"Failed to generate docstring for class: {class_name}. LLM service might have issues.")
            else:
                logger.warning(f"LLM returned empty docstring for class: {class_name}")
        else:
            logger.info(f"Skipping docstring for class '{class_name}' as it already exists and override is False.")
            
        self.current_class_name = None
        return updated_node

    def leave_FunctionDef(self, original_node, updated_node):
        """Check if the function already has a docstring and add one if needed, or if override is True.

        Args:
            original_node (cst.FunctionDef): The original AST node representing the function definition.
            updated_node (cst.FunctionDef): The updated AST node representing the function definition.

        Returns:
            cst.FunctionDef: The updated AST node with the docstring added if necessary.
        """
        func_name = original_node.name.value
        is_method = self.current_class_name is not None
        code_type = "method" if is_method else "function"
        full_func_name = f"{self.current_class_name}.{func_name}" if is_method else func_name
        
        has_existing_docstring = self._has_docstring(original_node.body.body)
        logger.debug(f"Leaving {code_type}: {full_func_name}, override: {self.override}, has_docstring: {has_existing_docstring}")

        if self.override or not has_existing_docstring:
            function_code = self._get_code_without_decorators(original_node)
            if not function_code.strip(): # Avoid sending empty code to LLM
                logger.warning(f"Skipping docstring generation for {code_type} '{full_func_name}' as its parsable code is empty.")
                return updated_node

            docstring_text = self.llm.generate_docstring(function_code, code_type=code_type)

            if docstring_text and "Unable to generate docstring" not in docstring_text:
                logger.info(f"Generated docstring for {code_type}: {full_func_name}")
                docstring_node = cst.SimpleStatementLine(
                    body=[cst.Expr(value=cst.SimpleString(f'"""{docstring_text}"""'))]
                )
                
                current_body_elements = list(updated_node.body.body)
                if has_existing_docstring and self.override and current_body_elements and \
                   isinstance(current_body_elements[0], cst.SimpleStatementLine) and \
                   isinstance(current_body_elements[0].body[0], cst.Expr) and \
                   isinstance(current_body_elements[0].body[0].value, cst.SimpleString):
                    # Remove existing docstring
                    new_body = [docstring_node] + current_body_elements[1:]
                else:
                    new_body = [docstring_node] + current_body_elements
                
                updated_node = updated_node.with_changes(
                    body=updated_node.body.with_changes(body=new_body)
                )
            elif "Unable to generate docstring" in docstring_text:
                 logger.error(f"Failed to generate docstring for {code_type}: {full_func_name}. LLM service might have issues.")
            else:
                logger.warning(f"LLM returned empty docstring for {code_type}: {full_func_name}")
        else:
            logger.info(f"Skipping docstring for {code_type} '{full_func_name}' as it already exists and override is False.")
            
        return updated_node

    def _has_docstring(self, body):
        """Check if a given body has a docstring.

        Args:
            body (List[cst.BaseStatement]): The body of the function or class to check for a docstring.

        Returns:
            bool: True if the body contains a docstring, False otherwise.
        """
        if body and isinstance(body[0], cst.SimpleStatementLine):
            stmt = body[0].body[0]
            if isinstance(stmt, cst.Expr) and isinstance(stmt.value, cst.SimpleString):
                return True
        return False

    def _get_code_without_decorators(self, node):
        """Get the code of a function without decorators.

        Args:
            node (cst.FunctionDef): The function node containing decorators.

        Returns:
            str: The code of the function without decorators.
        """
        function_def = node.with_changes(decorators=[])
        module = cst.Module(body=[function_def])
        function_code = module.code
        return function_code

    def _get_class_code(self, node):
        """Extracts the code for a class, including its methods if present, for LLM context.
        Currently simplifies to just the class structure and __init__ if present.

        Args:
            node (cst.ClassDef): The class node to extract code from.

        Returns:
            str: The code representing the class.
        """
        # This can be made more sophisticated to include method signatures or full method bodies
        # For now, keeping it similar to previous logic for simplicity
        init_method = None
        other_body_elements = []
        for element in node.body.body:
            if isinstance(element, cst.FunctionDef) and element.name.value == "__init__":
                init_method = element.with_changes(decorators=[])
            # Optionally, include other elements like assignments or simple statements
            # elif not isinstance(element, cst.FunctionDef): 
            #     other_body_elements.append(element)

        body_elements_for_llm = []
        if init_method:
            body_elements_for_llm.append(init_method)
        # body_elements_for_llm.extend(other_body_elements)
        
        if not body_elements_for_llm: # If no __init__ or other elements, add a pass
             body_elements_for_llm.append(cst.SimpleStatementLine(body=[cst.Pass()]))

        class_def_for_llm = node.with_changes(
            bases=[], # Consider if bases are important for context
            decorators=[], 
            body=node.body.with_changes(body=body_elements_for_llm)
        )
        module = cst.Module(body=[class_def_for_llm])
        return module.code


class ClassOrFunctionFinder(cst.CSTVisitor):
    """A class that identifies the presence of classes or functions within a codebase."""
    def __init__(self):
        self.has_class_or_function = False

    def visit_ClassDef(self, node):
        self.has_class_or_function = True
        return False # Stop traversal

    def visit_FunctionDef(self, node):
        self.has_class_or_function = True
        return False # Stop traversal


def add_docstrings_to_code(source_code, file_path, override=False, provider="openai", model_name=None):
    """Add docstrings to classes and functions in Python source code.

    Args:
        source_code (str): The source code to analyze and add docstrings to.
        file_path (str): The path to the file containing the source code (for logging).
        override (bool, optional): Whether to override existing docstrings. Defaults to False.
        provider (str, optional): The AI provider to use. Defaults to "openai".
        model_name (str, optional): The model name to use. Defaults to None (LLM class will handle default).

    Returns:
        str: The modified source code with added docstrings, or original if no changes.
    """
    logger.debug(f"Parsing code from file: {file_path}")
    try:
        module = cst.parse_module(source_code)
    except cst.ParserSyntaxError as e:
        logger.error(f"Syntax error parsing file '{file_path}': {e}")
        return source_code # Return original code on syntax error

    # Check if the file is essentially empty or only comments/module-level docstrings
    # A more robust check might be needed, but this is a basic one.
    is_empty_or_trivial = True
    for stmt in module.body:
        if not isinstance(stmt, (cst.EmptyLine, cst.Comment)):
            if isinstance(stmt, cst.SimpleStatementLine) and \
               isinstance(stmt.body[0], cst.Expr) and \
               isinstance(stmt.body[0].value, cst.SimpleString): # Module docstring
                continue 
            is_empty_or_trivial = False
            break
    if is_empty_or_trivial:
        logger.info(f"File '{file_path}' is empty or contains only comments/module docstring. Skipping docstring generation.")
        return source_code

    class_or_function_finder = ClassOrFunctionFinder()
    module.visit(class_or_function_finder)

    if not class_or_function_finder.has_class_or_function:
        logger.info(f"File '{file_path}' does not contain classes or functions to document. Skipping.")
        return source_code

    transformer = DocstringAdder(override=override, provider=provider, model_name=model_name)
    modified_tree = module.visit(transformer)
    return modified_tree.code


def add_docstrings_to_file(file_path, override=False, provider="openai", model_name=None):
    """Add docstrings to the functions in a Python file and write them back to the file.

    Args:
        file_path (str): The path to the Python file to process.
        override (bool, optional): Whether to override existing docstrings. Defaults to False.
        provider (str, optional): The AI provider to use. Defaults to "openai".
        model_name (str, optional): The model name to use. Defaults to None.
    """
    logger.info(f"Processing file: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return
    except Exception as e:
        logger.error(f"Error reading file '{file_path}': {e}")
        return

    if not source_code.strip():
        logger.info(f"File '{file_path}' is empty. Skipping.")
        return

    modified_code = add_docstrings_to_code(
        source_code, file_path, override, provider=provider, model_name=model_name
    )

    if modified_code == source_code:
        logger.info(f"No changes made to file (or file skipped): {file_path}")
        return
    
    logger.debug(f"Validating changes for file: {file_path}")
    if validate_only_docstrings_added(source_code, modified_code):
        logger.info(f"Docstrings generated for: {file_path}. Validation passed.")
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(modified_code)
            logger.info(f"Changes written to file: {file_path}")
        except Exception as e:
            logger.error(f"Error writing changes to file '{file_path}': {e}")
    else:
        logger.warning(
            f"Validation failed for file '{file_path}'. Code was modified beyond adding docstrings. Changes not written."
        )


def is_excluded(file_path, exclude_patterns):
    """Check if a file path is excluded based on a list of patterns.
    (This function seems unused in the current context of docstring_adder.py,
     as exclusion is handled in cli.py. If it's meant to be used here,
     it would need `logger` too.)

    Args:
        file_path (str): The file path to check for exclusion.
        exclude_patterns (list): A list of patterns to match against the file path.

    Returns:
        bool: True if the file path is excluded by any of the patterns, False otherwise.
    """
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(os.path.abspath(file_path), os.path.abspath(pattern)):
            # logger.debug(f"File '{file_path}' excluded by pattern '{pattern}'") # If logging is added here
            return True
    return False
