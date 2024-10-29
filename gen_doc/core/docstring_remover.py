import libcst as cst


class DocstringRemover(cst.CSTTransformer):
    """A class that removes docstrings from Python code."""

    def leave_Module(self, original_node, updated_node):
        """Remove the module docstring from the updated node.

        Args:
            self: The instance of the class.
            original_node (Node): The original node representing the module.
            updated_node (Node): The updated node representing the module with potential changes.

        Returns:
            Node: The updated node with the module docstring removed.

        Raises:
            None.
        """
        if self._has_docstring(updated_node.body):
            new_body = updated_node.body[1:]
            updated_node = updated_node.with_changes(body=new_body)
        return updated_node

    def leave_ClassDef(self, original_node, updated_node):
        """Remove the docstring from a ClassDef node.

        Args:
            self: The object instance.
            original_node (ast.ClassDef): The original ClassDef node.
            updated_node (ast.ClassDef): The updated ClassDef node with a docstring.

        Returns:
            ast.ClassDef: The updated ClassDef node without the docstring.

        Raises:
            None.
        """
        if self._has_docstring(updated_node.body.body):
            new_body = updated_node.body.body[1:]
            updated_node = updated_node.with_changes(
                body=updated_node.body.with_changes(body=new_body)
            )
        return updated_node

    def leave_FunctionDef(self, original_node, updated_node):
        """Removes the docstring from a function definition node.

        Args:
            self: The instance of the class.
            original_node (ast.FunctionDef): The original function definition node.
            updated_node (ast.FunctionDef): The updated function definition node.

        Returns:
            ast.FunctionDef: The updated function definition node with the docstring removed.

        Raises:
            None.
        """
        if self._has_docstring(updated_node.body.body):
            new_body = updated_node.body.body[1:]
            updated_node = updated_node.with_changes(
                body=updated_node.body.with_changes(body=new_body)
            )
        return updated_node

    def _has_docstring(self, body):
        """Check if a given body has a docstring.

        Args:
            self: The object instance.
            body (List[cst.BaseStatement]): The body of the function or class to check for a docstring.

        Returns:
            bool: True if the body contains a docstring, False otherwise.

        Raises:
            None.
        """
        if body and isinstance(body[0], cst.SimpleStatementLine):
            stmt = body[0].body[0]
            if isinstance(stmt, cst.Expr) and isinstance(stmt.value, cst.SimpleString):
                return True
        return False
