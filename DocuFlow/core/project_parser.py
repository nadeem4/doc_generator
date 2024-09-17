import os
from .python_parser import PythonParser

class ProjectParser:
    def __init__(self, root_directory: str):
        self.root_directory = root_directory
        self.project_data = []

    def find_python_files(self):
        python_files = []
        for root, dirs, files in os.walk(self.root_directory):
            for file in files:
                if file.endswith(".py"):
                    python_files.append(os.path.join(root, file))
        return python_files

    def parse_file(self, file_path: str):
        with open(file_path, "r") as file:
            code = file.read()
        parser = PythonParser()
        parser.parse(code)
        return {
            'file': file_path,
            'parsed_info': parser.get_parsed_info()
        }

    def parse_project(self):
        python_files = self.find_python_files()
        for file_path in python_files:
            parsed_file_info = self.parse_file(file_path)
            self.project_data.append(parsed_file_info)

    def get_project_data(self):
        return self.project_data
