from docstring_generator.core.docstring_remover import DocstringRemover
import libcst as cst


def validate_only_docstrings_added(original_code, modified_code):
    # Parse original code into CST module
    original_module = cst.parse_module(original_code)
    # Remove docstrings from original module
    original_module_no_docstrings = original_module.visit(DocstringRemover())
    # Generate code from original module without docstrings
    original_code_no_docstrings = original_module_no_docstrings.code

    # Parse modified code into CST module
    modified_module = cst.parse_module(modified_code)
    # Remove docstrings from modified module
    modified_module_no_docstrings = modified_module.visit(DocstringRemover())
    # Generate code from modified module without docstrings
    modified_code_no_docstrings = modified_module_no_docstrings.code

    # Compare the code
    if original_code_no_docstrings == modified_code_no_docstrings:
        return True
    else:
        return False
