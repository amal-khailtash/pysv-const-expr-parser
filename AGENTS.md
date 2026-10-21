# Depot development guidance

## Purpose and public API

Parse SystemVerilog constant expressions using SLY 0.5. Preserve the public
`amal.eda.systemverilog.const_expr_parser` namespace, lexer/parser/error exports,
and `sv_expr_parser_repl` command. A future pyslang migration is deferred;
do not replace SLY or add pyslang to runtime dependencies without user direction.
Optional pyslang reference tests are comparison material, not evidence of SLY support.

## Environment and build

- Use uv for dependencies, locking, synchronization, and distribution builds.
  Package the pure Python namespace with uv_build; no native SystemC backend is needed.
- Honor existing UV_* environment settings. Do not change cache, index, interpreter,
  or installation settings without authorization.
- Python 3.14 is the baseline; .python-version selects the same version for local development.
- Keep committed files portable, preserve user changes, and ignore local AI/editor state.
  AGENTS.md and uv.lock must remain trackable.

## Implementation and documentation

- Keep SLY grammar decorators and repeated production methods intact.
- Document public behavior, parameters, results, and errors with Python docstrings.
- Maintain Sphinx usage/API documentation alongside public API changes.
- Distinguish implemented behavior from incomplete IEEE 1800 semantics, especially
  widths, signedness, four-state values, and unfinished grammar productions.
- Preserve third-party MIT attribution in visitor.py and the project LICENSE.

## Validation

- Run targeted SLY tests after parser changes; test values, precedence, and errors.
- Run make lint, make test, make docs, and make build before publishing changes.
- Run optional comparisons with uv run --extra slang pytest tests/reference explicitly.
  Report their failures separately and never silently count them as SLY coverage.
- Check wheel installation and the installed console entry point outside the source tree.
- Report failures and unsupported features clearly; do not hide them behind skips.

## Releases and services

Use conventional commits and Release Please. Publish immutable version tags via
the manual publish workflow after configuring PyPI trusted publishing.
Codecov and Read the Docs integration require the owner to connect the repository;
never commit service tokens or local credentials.
