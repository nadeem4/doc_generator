import os
import sys
import argparse
from docstring_generator.core.docstring_adder import add_docstrings_to_file, is_excluded


def main():
    parser = argparse.ArgumentParser(description="Add docstrings to Python code.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-p", "--project", type=str, help="Path to the project directory."
    )
    group.add_argument("-f", "--file", type=str, help="Path to a single Python file.")
    parser.add_argument(
        "--exclude",
        nargs="*",
        default=[],
        help="List of files or patterns to exclude from processing.",
    )
    parser.add_argument(
        "--override", action="store_true", help="Override existing docstrings."
    )

    args = parser.parse_args()
    exclude_patterns = args.exclude

    if args.file:
        file_path = args.file
        if os.path.isfile(file_path) and file_path.endswith(".py"):
            if not is_excluded(file_path, exclude_patterns):
                add_docstrings_to_file(file_path, override=args.override)
            else:
                print(f"File '{file_path}' is excluded and will be skipped.")
        else:
            print(f"File '{file_path}' does not exist or is not a Python file.")
            sys.exit(1)
    elif args.project:
        project_path = args.project
        if os.path.isdir(project_path):
            for root, _, files in os.walk(project_path):
                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(root, file)
                        if not is_excluded(file_path, exclude_patterns):
                            add_docstrings_to_file(file_path, override=args.override)
                        else:
                            print(
                                f"File '{file_path}' is excluded and will be skipped."
                            )
        else:
            print(f"Directory '{project_path}' does not exist.")
            sys.exit(1)


if __name__ == "__main__":
    main()
