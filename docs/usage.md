# Usage

Install the project from a checkout with `uv sync --locked` and launch
`uv run sv_expr_parser_repl`. The module command
`uv run python -m amal.eda.systemverilog.const_expr_parser` starts the same REPL.

```python
from amal.eda.systemverilog.const_expr_parser import (
    ConstantExpressionLexer,
    ConstantExpressionParser,
)

lexer = ConstantExpressionLexer()
parser = ConstantExpressionParser()
assert parser.parse(lexer.tokenize("2 + 3 * 4")) == 14
```

Use `help` or `?` in the REPL; `quit`, `exit`, Ctrl+D, or Ctrl+C ends it.
Syntax errors raise `ConstantExpressionParseError` in the library and are printed
as diagnostics in the REPL.

## Current limitations

The grammar reference in [Annex E](AnnexE.md) defines expression syntax;
it is not a supported-feature checklist. Some productions still return grammar
objects. Numeric width, signedness, unknown/high-impedance digits, integer division,
and reduction semantics need further validation. Python results must not be
assumed equivalent to a full SystemVerilog elaborator.

The parser and REPL use SLY. Optional pyslang reference tests do not change the
runtime backend.

## Use from pyipxact-de

Add `pysv-const-expr-parser` to pyipxact-de's project dependencies once a release
is available. Until then, uv can use this repository as a Git or local path source.
Import the public lexer, parser, and `ConstantExpressionParseError` shown above.
Pass expression strings to `parser.parse(lexer.tokenize(text))` and handle parse
errors at the caller boundary. Parameter-name resolution and full SystemVerilog
elaboration are not yet a stable supported contract.
