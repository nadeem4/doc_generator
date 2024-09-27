import ast
import astor
from core.python_parser import DocstringAdder


def add_docstrings(source_code):
    """Add docstrings to functions, methods, and classes without changing any code."""
    tree = ast.parse(source_code)

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
    with open(filename, "r") as f:
        source_code = f.read()
    new_code = add_docstrings(source_code)
    with open(filename, "w") as f:
        f.write(new_code)
    print(f"Docstrings added to {filename}")
