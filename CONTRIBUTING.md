# Contributing

Use Python 3.14, uv, and the checked-in lockfile. Start with `make setup`, then
run `make lint`, `make test`, `make docs`, and `make build test-wheel`.
`make help` lists dependency, coverage, formatting, and published-package checks.

Use contributor branches such as `fix/literal-width` and Conventional Commit PR
titles such as `fix: report invalid expressions`. Add semantic SLY regression tests
for parser changes. Keep grammar references and implemented support distinct;
pyslang comparisons remain optional.

The [development guide](docs/development.md) describes the actual GitHub workflows,
branch/PR conventions, release process, manual PyPI publication, and hosted service
setup. The [release notes](docs/release_notes.md) include the shared changelog.
Never commit credentials or local AI/editor state.
