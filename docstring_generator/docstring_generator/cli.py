import os
import argparse
from docstring_generator.core.docstring_adder import add_docstrings_to_file, is_excluded
import concurrent.futures


def process_file(args):
    file_path, override = args
    add_docstrings_to_file(file_path, override=override)


def main():
    parser = argparse.ArgumentParser(
        description="Automatically generate docstrings for Python code."
    )
    parser.add_argument("paths", nargs="+", help="File or directory paths to process.")
    parser.add_argument("--exclude", nargs="*", default=[], help="Patterns to exclude.")
    parser.add_argument(
        "--override", action="store_true", help="Override existing docstrings."
    )
    args = parser.parse_args()

    # Collect all Python files to process
    files_to_process = []
    for path in args.paths:
        if os.path.isfile(path):
            if not is_excluded(path, args.exclude) and path.endswith(".py"):
                files_to_process.append((path, args.override))
        else:
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(root, file)
                        if not is_excluded(file_path, args.exclude):
                            files_to_process.append((file_path, args.override))

    # Process files in parallel
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(process_file, files_to_process)
