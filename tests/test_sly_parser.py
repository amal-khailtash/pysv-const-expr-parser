"""Semantic regression tests for the production SLY backend."""

import pytest

from amal.eda.systemverilog.const_expr_parser import (
    ConstantExpressionLexer,
    ConstantExpressionParser,
    ConstantExpressionParseError,
)
from amal.eda.systemverilog.const_expr_parser.repl import Repl


@pytest.mark.parametrize(
    "expression, expected",
    [
        ("42", 42),
        ("8'hff", 255),
        ("4'b1010", 10),
        ("2 + 3 * 4", 14),
        ("(2 + 3) * 4", 20),
        ("-5", -5),
        ("1 < 2", True),
        ("8 << 2", 32),
        ("$clog2(16)", 4),
    ],
)
def test_evaluation(expression, expected):
    """Assert literal values and arithmetic/operator precedence using SLY."""
    result = ConstantExpressionParser().parse(ConstantExpressionLexer().tokenize(expression))
    assert result == expected


def test_incomplete_expression():
    """Library consumers receive a parse error for truncated input."""
    with pytest.raises(ConstantExpressionParseError, match="EOF"):
        ConstantExpressionParser().parse(ConstantExpressionLexer().tokenize("1 +"))


def test_repl_evaluation(capsys):
    """The REPL evaluates with the library backend without an interactive terminal."""
    repl = Repl.__new__(Repl)
    assert repl.evaluate("2 + 3 * 4") == 14
    assert "Value: 14" in capsys.readouterr().out
    assert repl.evaluate("1 +") is None
    assert "Parse/Eval Error" in capsys.readouterr().out
