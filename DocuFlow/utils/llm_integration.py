import os
import pprint
from typing import List
from transformers import pipeline
from core.project_parser import ProjectParser

class ProjectLLMIntegration:
    def __init__(self, project_data: List[dict], llm_model="gpt-j-6B"):
        """Initialize with parsed project data and LLM model."""
        self.project_data = project_data
        self.llm = pipeline("text-generation", model=llm_model)

    def generate_readme(self):
        """Generate a README.md file using LLM based on the project data."""
        prompt = self.create_readme_prompt()
        response = self.llm(prompt, max_length=500)
        readme_content = response[0]["generated_text"]
        with open("README.md", "w") as readme_file:
            readme_file.write(readme_content)
        print("README.md generated successfully.")

    def create_readme_prompt(self):
        """Create a prompt for README generation."""
        summary = "Summary of the Project:\n"
        for file_info in self.project_data:
            summary += f"File: {file_info['file']}\n"
            if 'classes' in file_info['parsed_info']:
                summary += f"Classes: {len(file_info['parsed_info']['classes'])}\n"
            if 'functions' in file_info['parsed_info']:
                summary += f"Functions: {len(file_info['parsed_info']['functions'])}\n"
        prompt = f"Based on the following information, generate a detailed README:\n{summary}"
        return prompt

    def generate_docstrings(self):
        """Generate docstrings for each function, method, and class using LLM."""
        for file_info in self.project_data:
            updated_code = self.create_docstrings_for_file(file_info)
            file_path = file_info['file']
            with open(file_path, "w") as code_file:
                code_file.write(updated_code)
            print(f"Docstrings added to {file_path}")

    def create_docstrings_for_file(self, file_info):
        """Create docstrings for all functions, methods, and classes in a file."""
        updated_code = ""
        for class_info in file_info["parsed_info"]["classes"]:
            class_prompt = self.create_class_docstring_prompt(class_info)
            response = self.llm(class_prompt, max_length=200)
            docstring = response[0]["generated_text"]
            updated_code += f'"""{docstring}"""\n{class_info["definition"]}\n'

            # Add docstrings to methods
            for method_info in class_info["methods"]:
                method_prompt = self.create_method_docstring_prompt(method_info)
                response = self.llm(method_prompt, max_length=150)
                method_docstring = response[0]["generated_text"]
                updated_code += f'"""{method_docstring}"""\n{method_info["definition"]}\n'

        # Add docstrings to functions
        for function_info in file_info["parsed_info"]["functions"]:
            function_prompt = self.create_function_docstring_prompt(function_info)
            response = self.llm(function_prompt, max_length=150)
            function_docstring = response[0]["generated_text"]
            updated_code += f'"""{function_docstring}"""\n{function_info["definition"]}\n'
        
        return updated_code

    def create_class_docstring_prompt(self, class_info):
        """Create a prompt to generate a docstring for a class."""
        prompt = f"Generate a docstring for the following class:\n{class_info['definition']}\n"
        return prompt

    def create_method_docstring_prompt(self, method_info):
        """Create a prompt to generate a docstring for a method."""
        prompt = f"Generate a docstring for the following method:\n{method_info['definition']}\n"
        return prompt

    def create_function_docstring_prompt(self, function_info):
        """Create a prompt to generate a docstring for a function."""
        prompt = f"Generate a docstring for the following function:\n{function_info['definition']}\n"
        return prompt

    def generate_code_flow_document(self):
        """Generate a high-level code flow document using the parsed data."""
        flow_content = "### Code Flow Documentation\n"
        for file_info in self.project_data:
            flow_content += f"File: {file_info['file']}\n"
            for class_info in file_info['parsed_info']['classes']:
                flow_content += f"Class: {class_info['name']}\n"
                for method_info in class_info['methods']:
                    flow_content += f"  Method: {method_info['name']}\n"
            for function_info in file_info['parsed_info']['functions']:
                flow_content += f"Function: {function_info['name']}\n"
        with open("code_flow.md", "w") as flow_file:
            flow_file.write(flow_content)
        print("Code flow document created.")

    def generate_contribution_guide(self):
        """Generate CONTRIBUTING.md with contribution guidelines."""
        prompt = "Generate a contribution guide for a Python project that includes reporting issues, submitting pull requests, and coding style guidelines."
        response = self.llm(prompt, max_length=400)
        contribution_content = response[0]["generated_text"]
        with open("CONTRIBUTING.md", "w") as contribution_file:
            contribution_file.write(contribution_content)
        print("CONTRIBUTING.md created.")


# Usage Example
if __name__ == "__main__":
    project_parser = ProjectParser("my_project")
    project_parser.parse_project()
    
    llm_integration = ProjectLLMIntegration(project_parser.get_project_data())
    
    # Generate README
    llm_integration.generate_readme()

    # Add docstrings to classes, methods, and functions
    llm_integration.generate_docstrings()

    # Generate code flow document
    llm_integration.generate_code_flow_document()

    # Generate CONTRIBUTING.md
    llm_integration.generate_contribution_guide()
