# pysv-const-expr-parser

[![CI](https://github.com/amal-khailtash/pysv-const-expr-parser/actions/workflows/ci.yml/badge.svg)](https://github.com/amal-khailtash/pysv-const-expr-parser/actions/workflows/ci.yml)
[![Codecov](https://codecov.io/gh/amal-khailtash/pysv-const-expr-parser/branch/main/graph/badge.svg)](https://codecov.io/gh/amal-khailtash/pysv-const-expr-parser)
[![Documentation](https://readthedocs.org/projects/pysv-const-expr-parser/badge/?version=latest)](https://pysv-const-expr-parser.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A Python SystemVerilog constant expression parser using **SLY 0.5**.
The implementation is experimental; IEEE 1800 support is incomplete, particularly
width/signedness propagation, four-state values, and unfinished productions.
The current evaluator can use Python numeric semantics where SystemVerilog differs.
SLY remains the default backend. A possible future pyslang migration is deferred.

## Development

Install [uv](https://docs.astral.sh/uv/), then:

```sh
uv sync --locked --all-groups
uv run sv_expr_parser_repl
# Also available as:
uv run python -m amal.eda.systemverilog.const_expr_parser
```

Python 3.13+ is supported; local development selects 3.14.

```python
from amal.eda.systemverilog.const_expr_parser import (
    ConstantExpressionLexer,
    ConstantExpressionParser,
)

value = ConstantExpressionParser().parse(ConstantExpressionLexer().tokenize("2 + 3 * 4"))
assert value == 14
```

```sh
make lint
make test
make coverage
make docs
make build
```

The distribution uses a `src/` namespace layout under
`amal.eda.systemverilog.const_expr_parser` and the uv_build backend.
See [CONTRIBUTING.md](CONTRIBUTING.md) for release and hosted service setup.

## Grammar and documentation

[docs/AnnexE.md](docs/AnnexE.md) contains the SystemVerilog expression syntax
reference. It describes the grammar, not a guarantee that every production is
implemented. Sphinx includes this reference alongside usage and API documentation.

## Optional pyslang comparisons

Existing pyslang tests are retained as reference material and excluded from the
default SLY suite. To run them explicitly:

```sh
uv run --extra slang pytest tests/reference
```

Their results do not measure SLY support or coverage.

## License

MIT; see [LICENSE](LICENSE). Third-party visitor attribution is preserved in its source.
