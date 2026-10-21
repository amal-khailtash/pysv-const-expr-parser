# Contributing

Use uv and the checked-in lockfile. Run `make setup`, then `make lint`,
`make test`, `make docs`, and `make build`. Use conventional commit titles
such as `fix: handle invalid expressions` or `docs: explain literal syntax`.
Add semantic SLY regression tests for parser changes. Keep grammar references
and implemented support distinct; pyslang comparisons remain optional.

## Releases

Release Please maintains the changelog and version through a release PR.
Set `RELEASE_PLEASE_TOKEN` to a suitably scoped personal or GitHub App token so
release PRs trigger CI. After reviewing and merging a release PR, dispatch
`publish.yml` with its immutable `vX.Y.Z` tag. The workflow reruns CI, checks
that the tag matches project metadata and belongs to main, and publishes the
validated distributions. Configure the `pypi` GitHub environment and a PyPI
trusted publisher for this owner/repository, `publish.yml`, and that environment.
Publication is manual; no package is uploaded by scaffold creation.

## Hosted services

- Connect the repository in Codecov and add the `CODECOV_TOKEN` repository secret
  if required by your Codecov account. CI uploads XML from the SLY suite.
  Upload failures are informational while service onboarding is incomplete.
- Import the repository at Read the Docs with the project slug
  `pysv-const-expr-parser`. The committed `.readthedocs.yaml` builds Sphinx
  with warnings treated as errors. Documentation URLs and badges become live
  after this import and a successful build.
- Enable GitHub Actions. Release Please requires permission to create pull requests.

Never commit credentials. Local AI/editor state is ignored; AGENTS.md is shared.

## Common Make tasks

Python 3.14 is required. `make help` lists the available tasks, including
`uv-lock`, `uv-sync`, `uv-sync-upgrade`, `uv-list-outdated`, and `format-python`.
Use `make test TEST_ARGS="-k evaluation"` for targeted checks.
`make build test-wheel` verifies the installed distribution outside the checkout.
Override `WHEEL_DIR` to select a build directory. Once a release is published,
use `make test-pypi PACKAGE_VERSION=X.Y.Z` or `make test-testpypi PACKAGE_VERSION=X.Y.Z`.
`make vars` and `make var-PACKAGE_VERSION` display build settings.
