import os

def add_code_snippet(code, language='python'):
    return f"```{language}\n{code}\n```\n\n"

def generate_markdown(classes, functions, filepath, output_dir):
    # Create output file name based on the file being documented
    filename = os.path.basename(filepath).replace('.py', '.md')
    output_path = os.path.join(output_dir, filename)
    
    md_content = f"# Documentation for `{filepath}`\n\n"

    if classes:
        md_content += "## Classes\n\n"
        for cls in classes:
            md_content += f"### `{cls['name']}`\n\n"
            if cls['docstring']:
                md_content += f"{cls['docstring']}\n\n"
            # Optionally include class definition
            class_def = f"class {cls['name']}:\n    pass  # Implementation"
            md_content += add_code_snippet(class_def) + "\n"
            
            if cls['methods']:
                md_content += "**Methods:**\n\n"
                for method in cls['methods']:
                    md_content += f"- `{method['name']}()`\n"
                    if method['docstring']:
                        md_content += f"  - {method['docstring']}\n"
                md_content += "\n"

    if functions:
        md_content += "## Functions\n\n"
        for func in functions:
            md_content += f"### `{func['name']}()`\n\n"
            if func['docstring']:
                md_content += f"{func['docstring']}\n\n"
            # Optionally include function definition
            func_def = f"def {func['name']}():\n    pass  # Implementation"
            md_content += add_code_snippet(func_def) + "\n"

    # Write to a Markdown file
    with open(output_path, 'w', encoding='utf-8') as md_file:
        md_file.write(md_content)

    print(f"Generated documentation for {filepath} at {output_path}")
