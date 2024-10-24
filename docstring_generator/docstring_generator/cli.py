import os
import argparse
from docstring_generator.core.docstring_adder import add_docstrings_to_file, is_excluded
import concurrent.futures


def process_file(args):
    """Process a file by adding docstrings to it.

    Args:
        args (tuple): A tuple containing the file path (str) and a boolean flag (bool) indicating whether to override existing docstrings.

    Returns:
        None

    Raises:
        FileNotFoundError: If the file specified in the file path does not exist.
        PermissionError: If the file specified in the file path cannot be accessed due to permission issues.
        ValueError: If invalid arguments are provided in the args tuple.
    """
    file_path, override = args
    add_docstrings_to_file(file_path, override=override)


def main():
    """Automatically generate docstrings for Python code.

    This function parses command-line arguments to process file or directory paths and optionally set an OpenAI API key as an environment variable.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
    parser = argparse.ArgumentParser(
        description="Automatically generate docstrings for Python code."
    )
    parser.add_argument("paths", nargs="+", help="File or directory paths to process.")
    parser.add_argument("--exclude", nargs="*", default=[], help="Patterns to exclude.")
    parser.add_argument(
        "--override", action="store_true", help="Override existing docstrings."
    )
    parser.add_argument("--apikey", help="OpenAI API key.")
    args = parser.parse_args()

    # Set the API key to environment variable if provided
    if args.apikey:
        os.environ["OPENAI_API_KEY"] = args.apikey
    args = parser.parse_args()

    # Collect all Python files to process
    files_to_process = []
    for path in args.paths:
        if os.path.isfile(path):
            if not is_excluded(path, args.exclude) and path.endswith(".py"):
                add_docstrings_to_file(path, override=args.override)
        else:
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(root, file)
                        if not is_excluded(file_path, args.exclude):
                            # files_to_process.append((file_path, args.override))
                            add_docstrings_to_file(file_path, override=args.override)
