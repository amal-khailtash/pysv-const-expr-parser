"""Interactive SystemVerilog constant expression evaluation using SLY."""

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.hdl import SystemVerilogLexer

from . import ConstantExpressionLexer, ConstantExpressionParser, ConstantExpressionParseError

HELP = """SystemVerilog Constant Expression REPL (SLY backend)
Enter an expression to evaluate; '?' or 'help' for help; 'quit' or 'exit' to leave.
Press Ctrl+D or Ctrl+C to exit. IEEE 1800 support is incomplete.
"""


class Repl:
    """Evaluate expressions with the library's SLY lexer and parser."""

    def __init__(self):
        """Create an interactive prompt with in-memory history."""
        self.session = PromptSession(
            "sv const expr > ",
            history=InMemoryHistory(),
            auto_suggest=AutoSuggestFromHistory(),
            lexer=PygmentsLexer(SystemVerilogLexer),
        )

    def evaluate(self, text: str):
        """Parse text and print its value or diagnostic; return the parsed result."""
        try:
            result = ConstantExpressionParser().parse(ConstantExpressionLexer().tokenize(text))
        except (ConstantExpressionParseError, ValueError, ArithmeticError) as error:
            print(f"Parse/Eval Error: {error}")
            return None
        if isinstance(result, int):
            print(f"Value: {result:,} (dec), {result:b} (bin), {result:o} (oct), {result:x} (hex)")
        else:
            print(f"Value: {result}")
        return result

    def run(self):
        """Read and evaluate expressions until exit or a keyboard interrupt."""
        print(HELP)
        while True:
            try:
                text = self.session.prompt().strip()
            except EOFError, KeyboardInterrupt:
                break
            if text in ("quit", "exit"):
                break
            if text in ("?", "help"):
                print(HELP)
            elif text:
                self.evaluate(text)


def main():
    """Run the SLY expression REPL."""
    Repl().run()


if __name__ == "__main__":
    main()
