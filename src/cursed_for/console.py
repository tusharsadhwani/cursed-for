import code
from contextlib import suppress

from cursed_for.errors import CursedEOFError


class CursedConsole(code.InteractiveConsole):
    def runsource(
        self,
        source: str,
        filename: str = "<input>",
        symbol: str = "single",
    ) -> bool:
        try:
            actual_source = source.encode("utf-8").decode("cursed_for")
        except CursedEOFError:
            return True

        with suppress(SyntaxError, OverflowError):
            if code.compile_command(actual_source) == None:
                return True

        code_obj = compile(actual_source, filename, mode="exec")
        self.runcode(code_obj)
        return False
