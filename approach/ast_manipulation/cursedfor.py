"""
The original cursed-for implementation.

Works only inside the REPL started by this file.

Here's how you use it:

    $ python cursedfor.py
    Cursed Python REPL, 3.10.4 (main, Apr  2 2022, 09:04:19) [GCC 11.2.0]
    >>> with _for(i := 0, i < 10, i + 2):
    ...     print(i)
    0
    2
    4
    6
    8
    >>>
"""
import ast
import code
from contextlib import suppress
import sys
from typing import List


class ForTransformer(ast.NodeTransformer):
    @staticmethod
    def is_cursed_for_call(node: ast.AST) -> bool:
        return (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "_for"
        )

    def generic_visit(self, node: ast.AST) -> ast.AST:
        super().generic_visit(node)

        if hasattr(node, "body") and isinstance(node.body, list):
            new_body = []
            for item in node.body:
                if not isinstance(item, ast.With):
                    new_body.append(item)
                    continue

                if not any(
                    self.is_cursed_for_call(expr.context_expr) for expr in item.items
                ):
                    new_body.append(item)
                    continue

                item_replacements = self.replace_cursed_for(item)
                new_body.extend(item_replacements)

            node.body = new_body

        return node

    def replace_cursed_for(self, node: ast.With) -> List[ast.AST]:
        if len(node.items) > 1:
            raise SyntaxError("Cursed-for doesn't support multi-with statements.")

        cursed_for_call: ast.Call = node.items[0].context_expr

        if len(cursed_for_call.args) != 3:
            raise SyntaxError(
                "Cursed for loops require the _for(init, condition, increment) format."
            )

        init_node, condition_node, increment_node = cursed_for_call.args
        if not isinstance(init_node, ast.NamedExpr):
            raise SyntaxError("First argument to for loop must be of type `x := value`")

        init_variable: ast.Name = init_node.target
        init_statement = ast.Assign(targets=[init_variable], value=init_node.value)

        if not (
            isinstance(condition_node, ast.Compare)
            and isinstance(condition_node.left, ast.Name)
            and condition_node.left.id == init_variable.id
        ):
            raise SyntaxError("First argument to for loop must be of type `x < value`")

        if not (
            isinstance(increment_node, ast.BinOp)
            and isinstance(condition_node.left, ast.Name)
            and condition_node.left.id == init_variable.id
        ):
            raise SyntaxError("First argument to for loop must be of type `x + inc`")

        increment_statement = ast.AugAssign(
            target=init_variable,
            op=increment_node.op,
            value=increment_node.right,
        )
        block_body = [*node.body, increment_statement]
        while_statement = ast.While(test=condition_node, body=block_body, orelse=[])
        return [init_statement, while_statement]


class CursedConsole(code.InteractiveConsole):
    def runsource(
        self,
        source: str,
        filename: str = "<input>",
        symbol: str = "single",
    ) -> bool:
        # First, check if it could be incomplete input, return True if it is.
        # This will allow it to keep taking input
        with suppress(SyntaxError, OverflowError):
            if code.compile_command(source) == None:
                return True

        try:
            tree = ast.parse(source, filename, mode=symbol)
            cursed_tree = ForTransformer().visit(tree)
            ast.fix_missing_locations(cursed_tree)
        except (ValueError, SyntaxError):
            # Let the original implementation take care of incomplete input / errors
            return super().runsource(source, filename, symbol)

        code_obj = compile(tree, filename, mode=symbol)
        self.runcode(code_obj)
        return False


def main():
    if sys.platform != "win32":
        import readline

        readline.parse_and_bind("tab: complete")

    CursedConsole().interact(banner=f"Cursed Python REPL, {sys.version}", exitmsg="")


if __name__ == "__main__":
    main()
