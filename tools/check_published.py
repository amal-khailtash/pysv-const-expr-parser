"""Verify an installed distribution and its console entry point outside the checkout."""

from importlib.metadata import distribution
import subprocess
import sys

from amal.eda.systemverilog.const_expr_parser import ConstantExpressionLexer, ConstantExpressionParser
from amal.eda.systemverilog.const_expr_parser.repl import main


def check(version: str) -> None:
    """Assert package version, SLY precedence, and installed REPL startup/exit."""
    package = distribution("pysv-const-expr-parser")
    assert package.version == version, package.version
    assert ConstantExpressionParser().parse(ConstantExpressionLexer().tokenize("2 + 3 * 4")) == 14
    entry = next(item for item in package.entry_points if item.name == "sv_expr_parser_repl")
    assert entry.load() is main
    result = subprocess.run(
        ["sv_expr_parser_repl"], input="quit\n", text=True, capture_output=True, timeout=15, check=True
    )
    assert "SLY backend" in result.stdout, result.stdout
    print(f"Installed {package.metadata['Name']} {version}: library and REPL passed")


if __name__ == "__main__":
    check(sys.argv[1])
