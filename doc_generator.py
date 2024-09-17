import argparse
from DocuFlow.file_traverser import run_doc_generator

def main():
    parser = argparse.ArgumentParser(description="Generate Markdown documentation from Python code.")
    parser.add_argument('project_path', help="Path to the Python project")
    parser.add_argument('--output', default='docs', help="Output directory for documentation")
    
    args = parser.parse_args()
    run_doc_generator(args.project_path, args.output)

if __name__ == "__main__":
    main()
