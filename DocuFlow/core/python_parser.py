import ast
import astor
from utils.llm import LLM

class DocstringAdder(ast.NodeTransformer):
        
        def __init__(self):
            self.llm = LLM()
            self.llm.initialize_client()


        def visit_FunctionDef(self, node):
            self.generic_visit(node)

            if ast.get_docstring(node) is None:
                # Check if this is a method (parent is a class) or a function
                if hasattr(node, 'parent') and isinstance(node.parent, ast.ClassDef):
                    # Method
                    node_copy = ast.FunctionDef(
                        name=node.name,
                        args=node.args,
                        body=node.body,
                        decorator_list=[],
                        returns=node.returns,
                        type_comment=node.type_comment,
                    )
                    method_code = astor.to_source(node_copy)
                    # Generate the docstring
                    docstring = self.llm.generate_docstring(method_code, code_type='method')
                else:
                    # Function
                    node_copy = ast.FunctionDef(
                        name=node.name,
                        args=node.args,
                        body=node.body,
                        decorator_list=[],
                        returns=node.returns,
                        type_comment=node.type_comment,
                    )
                    func_code = astor.to_source(node_copy)
                    # Generate the docstring
                    docstring = self.llm.generate_docstring(func_code, code_type='function')

                if docstring:
                    # Create a new docstring node
                    new_docstring = ast.Expr(value=ast.Constant(value=docstring))
                    # Insert the docstring at the beginning of the function body
                    node.body.insert(0, new_docstring)
            return node

        def visit_ClassDef(self, node):
            self.generic_visit(node)
            if ast.get_docstring(node) is None:
                # Include the __init__ method and attribute assignments
                init_method = next((n for n in node.body if isinstance(n, ast.FunctionDef) and n.name == '__init__'), None)
                if init_method:
                    # Create a copy of the __init__ method
                    init_method_copy = ast.FunctionDef(
                        name=init_method.name,
                        args=init_method.args,
                        body=init_method.body,
                        decorator_list=[],
                        returns=init_method.returns,
                        type_comment=init_method.type_comment,
                    )
                    # Create a simplified class node
                    node_copy = ast.ClassDef(
                        name=node.name,
                        bases=[],
                        keywords=[],
                        body=[init_method_copy],
                        decorator_list=[],
                    )
                else:
                    # If no __init__, create an empty class
                    node_copy = ast.ClassDef(
                        name=node.name,
                        bases=[],
                        keywords=[],
                        body=[ast.Pass()],
                        decorator_list=[],
                    )

                class_code = astor.to_source(node_copy)
                # Generate the docstring
                docstring = self.llm.generate_docstring(class_code, code_type='class')
                if docstring:
                    # Create a new docstring node
                    new_docstring = ast.Expr(value=ast.Constant(value=docstring))
                    # Insert the docstring at the beginning of the class body
                    node.body.insert(0, new_docstring)
            return node