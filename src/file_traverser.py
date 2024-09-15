import os
from .code_parser import parse_file
from .markdown_generator import generate_markdown

def traverse_directory(project_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                print(f"Processing file: {filepath}")
                classes, functions = parse_file(filepath)
                generate_markdown(classes, functions, filepath, output_dir)

def run_doc_generator(project_path, output_dir):
    print(f"Starting documentation generation for project: {project_path}")
    traverse_directory(project_path, output_dir)
    print(f"Documentation generated in directory: {output_dir}")
