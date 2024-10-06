import libcst as cst


class DocstringRemover(cst.CSTTransformer):
    def leave_Module(self, original_node, updated_node):
        if self._has_docstring(updated_node.body):
            new_body = updated_node.body[1:]  # Remove the module docstring
            updated_node = updated_node.with_changes(body=new_body)
        return updated_node

    def leave_ClassDef(self, original_node, updated_node):
        if self._has_docstring(updated_node.body.body):
            new_body = updated_node.body.body[1:]  # Remove the docstring
            updated_node = updated_node.with_changes(
                body=updated_node.body.with_changes(body=new_body)
            )
        return updated_node

    def leave_FunctionDef(self, original_node, updated_node):
        if self._has_docstring(updated_node.body.body):
            new_body = updated_node.body.body[1:]  # Remove the docstring
            updated_node = updated_node.with_changes(
                body=updated_node.body.with_changes(body=new_body)
            )
        return updated_node

    def _has_docstring(self, body):
        if body and isinstance(body[0], cst.SimpleStatementLine):
            stmt = body[0].body[0]
            if isinstance(stmt, cst.Expr) and isinstance(stmt.value, cst.SimpleString):
                return True
        return False
