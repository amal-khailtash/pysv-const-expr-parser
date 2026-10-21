# pysv-const-expr-parser

| Category | Status |
| --- | --- |
| CI/CD | [![01. PR title](https://github.com/amal-khailtash/pysv-const-expr-parser/actions/workflows/pr-title.yml/badge.svg)](https://github.com/amal-khailtash/pysv-const-expr-parser/actions/workflows/pr-title.yml) [![02. CI](https://github.com/amal-khailtash/pysv-const-expr-parser/actions/workflows/ci.yml/badge.svg)](https://github.com/amal-khailtash/pysv-const-expr-parser/actions/workflows/ci.yml) [![03. Release Please](https://github.com/amal-khailtash/pysv-const-expr-parser/actions/workflows/release-please.yml/badge.svg)](https://github.com/amal-khailtash/pysv-const-expr-parser/actions/workflows/release-please.yml) [![04. Publish](https://github.com/amal-khailtash/pysv-const-expr-parser/actions/workflows/publish.yml/badge.svg)](https://github.com/amal-khailtash/pysv-const-expr-parser/actions/workflows/publish.yml) |
| Project | [![GitHub](https://img.shields.io/badge/pysv-const-expr-parser-29b6f6?logo=github&labelColor=0277bd)](https://github.com/amal-khailtash/pysv-const-expr-parser) [![PyPI](https://img.shields.io/pypi/v/pysv-const-expr-parser?logo=pypi&logoColor=FBE072&cacheSeconds=300&release=0.1.0)](https://pypi.org/project/pysv-const-expr-parser/) [![GitHub tag](https://img.shields.io/github/v/tag/amal-khailtash/pysv-const-expr-parser?logo=github&label=version)](https://github.com/amal-khailtash/pysv-const-expr-parser/tags) |
| Docs | [![Read the Docs](https://readthedocs.org/projects/pysv-const-expr-parser/badge/?version=latest)](https://pysv-const-expr-parser.readthedocs.io/en/latest/) |
| Coverage | [![Codecov](https://codecov.io/gh/amal-khailtash/pysv-const-expr-parser/branch/main/graph/badge.svg)](https://codecov.io/gh/amal-khailtash/pysv-const-expr-parser) |
| Meta | [![License](https://img.shields.io/github/license/amal-khailtash/pysv-const-expr-parser)](https://github.com/amal-khailtash/pysv-const-expr-parser/blob/main/LICENSE) [![Stars](https://img.shields.io/github/stars/amal-khailtash/pysv-const-expr-parser)](https://github.com/amal-khailtash/pysv-const-expr-parser/stargazers) [![Forks](https://img.shields.io/github/forks/amal-khailtash/pysv-const-expr-parser)](https://github.com/amal-khailtash/pysv-const-expr-parser/forks) [![Contributors](https://img.shields.io/github/contributors/amal-khailtash/pysv-const-expr-parser)](https://github.com/amal-khailtash/pysv-const-expr-parser/graphs/contributors) |
| Standards | [![Python](https://img.shields.io/badge/python-3.13%2B-blue?logo=python)](https://www.python.org/) [![SemVer](https://img.shields.io/badge/SemVer-2.0.0-333333?logo=semver)](https://semver.org/) [![Keep a Changelog](https://img.shields.io/badge/Keep%20a%20Changelog-1.1.0-0c7fb0?logo=keepachangelog&logoColor=white)](https://keepachangelog.com/en/1.1.0/) [![Release Please v4](https://img.shields.io/badge/Release%20Please-v4-blue)](https://github.com/googleapis/release-please-action/tree/v4) |

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
