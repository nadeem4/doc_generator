import ast

class CodeParser(ast.NodeVisitor):
    def __init__(self):
        self.classes = []
        self.functions = []

    def visit_ClassDef(self, node):
        class_info = {
            'name': node.name,
            'docstring': ast.get_docstring(node),
            'methods': []
        }
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_info = {
                    'name': item.name,
                    'docstring': ast.get_docstring(item)
                }
                class_info['methods'].append(method_info)
        self.classes.append(class_info)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        func_info = {
            'name': node.name,
            'docstring': ast.get_docstring(node)
        }
        self.functions.append(func_info)
        self.generic_visit(node)

def parse_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=filepath)
    parser = CodeParser()
    parser.visit(tree)
    return parser.classes, parser.functions
