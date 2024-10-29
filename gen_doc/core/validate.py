from doc_craft.core.docstring_remover import DocstringRemover
import libcst as cst


def validate_only_docstrings_added(original_code, modified_code):
    """Validate if only docstrings have been added or modified in the code.

    Args:
        original_code (str): The original code to compare.
        modified_code (str): The modified code to compare.

    Returns:
        bool: True if only docstrings have been added or modified, False otherwise.

    Raises:
        None
    """
    original_module = cst.parse_module(original_code)
    original_module_no_docstrings = original_module.visit(DocstringRemover())
    original_code_no_docstrings = original_module_no_docstrings.code

    modified_module = cst.parse_module(modified_code)
    modified_module_no_docstrings = modified_module.visit(DocstringRemover())
    modified_code_no_docstrings = modified_module_no_docstrings.code

    if original_code_no_docstrings == modified_code_no_docstrings:
        return True
    else:
        return False
