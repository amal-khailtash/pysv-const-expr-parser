# Development

Use Python 3.14 and [uv](https://docs.astral.sh/uv/). The pure Python package uses
uv_build and retains SLY 0.5 as its parser backend. Existing `UV_*` settings are
honored. The library is intended for use by pyipxact-de; the REPL uses the same
lexer/parser API for local experiments.

## Environment and validation

```sh
make setup
make lint
make test
make coverage
make docs
make build test-wheel
```

`make setup` synchronizes all dependency groups from `uv.lock`. `make uv-lock`
refreshes the lock; `make uv-sync-upgrade` deliberately upgrades dependencies.
Use `make format-python` to format code and
`make test TEST_ARGS="-k evaluation"` for targeted regression checks.
`make help` lists tasks; `make vars` displays package and build settings.

SLY tests assert values, precedence, and error behavior. Coverage measures Python
code and writes XML to `build/coverage/coverage.xml` and HTML to
`build/coverage/html/index.html`. The installed-wheel check runs outside the
checkout and verifies library evaluation, the console entry point, and REPL exit.
Override `WHEEL_DIR` or `PACKAGE_VERSION` when checking another build.

Sphinx builds HTML in `build/docs` with warnings treated as errors. Keep usage,
API docs, and [release notes](release_notes.md) current. [Annex E](AnnexE.md)
is the expression syntax reference; it does not establish implemented support.
Widths, signedness, four-state values, and unfinished productions need further
validation. Add semantic SLY tests when extending supported behavior.

Optional pyslang comparisons live in `tests/reference` and are excluded from the
default suite:

```sh
uv run --extra slang pytest tests/reference
```

Their results do not measure SLY support or coverage. The two legacy test scripts
remain local and ignored. Do not replace SLY without an explicit migration decision.

## Branch and pull request conventions

Create contributor branches from current `main` using `<type>/<short-description>`,
for example `feat/parameter-resolution`, `fix/literal-width`, or
`docs/development-workflow`. Target pull requests at `main` and use a Conventional
Commit title such as `fix: report incomplete expressions`.

Validate locally, open the PR, and wait for the PR title and CI checks before
merging. Squash merging with the PR title gives Release Please a consistent commit
to classify. For changes spanning pyipxact-de and this parser, use separate PRs
and verify the integration in each repository.

## GitHub workflows

| Workflow | Trigger | Behavior |
| --- | --- | --- |
| `pr-title.yml` | PR opened, edited, synchronized, or reopened | Checks the Conventional Commit title using PR metadata; it does not check out PR code. |
| `ci.yml` | PRs, pushes to `main`, manual dispatch, or reusable workflow call | Runs Python 3.14 lint/tests/coverage, builds and checks distributions and the installed wheel, and validates Sphinx. |
| `release-please.yml` | Push to `main` or manual dispatch | Opens or updates a release PR; when its token is absent, reports a setup notice and skips automation. |
| `publish.yml` | Manual dispatch with an existing `vX.Y.Z` tag | Reruns CI against the tag, verifies the tag/version and ancestry, then publishes those CI artifacts to PyPI. |

CI stores `coverage-3.14`, `ci-distributions`, and `documentation` artifacts.
Codecov receives the SLY XML report; upload failures do not fail CI. The docs
job validates and archives HTML. Hosted documentation is built separately by
Read the Docs through its repository integration.

## Release and publication workflow

1. Merge validated contributor PRs with Conventional Commit titles. Release Please
   collects release-worthy changes into a generated release PR. `feat` and `fix`
   signal new functionality and fixes; mark breaking changes explicitly. Review
   the proposed version rather than assuming a particular pre-1.0 increment.
2. Review the generated version and changelog updates and wait for release PR CI.
   Check that `pyproject.toml` and `uv.lock` agree; regenerate the lockfile if needed.
   Leave the release PR open until ready to create the release.
3. Merge the release PR to create its version tag and GitHub release. This repository
   does **not** automatically dispatch package publication after the release.
4. From the Actions **Publish** workflow on `main`, dispatch the existing immutable
   tag, such as `v0.1.1`. The reusable CI runs against that tag and produces the
   distributions that will be uploaded.
5. Publication verifies that the supplied ref is a tag pointing at the checked-out
   commit, that it is an ancestor of `origin/main`, and that its name matches
   `v` plus the project version. The `pypi` environment job then uses uv trusted
   publishing to upload the validated distributions.
6. Inspect the PyPI result and the separate Read the Docs build. To smoke-check a
   published release, run `make test-pypi PACKAGE_VERSION=X.Y.Z`.

The publisher currently targets PyPI only. `make test-testpypi` checks a package
already uploaded to TestPyPI; it does not upload it. There is no automatic
post-publication Read the Docs API trigger in this repository.

PyPI versions and release tags are immutable. Inspect uploaded files before
retrying a partial publication. A workflow repair can be dispatched from `main`
with the same existing tag, while source and version remain tied to the tag.
Manual publication should be dispatched only when an upload is intended.

## Service setup

- Enable GitHub Actions and allow Actions to create pull requests. Configure
  `RELEASE_PLEASE_TOKEN` with appropriate contents and pull-request access so
  generated release PRs can trigger CI.
- Configure a PyPI trusted publisher for owner `amal-khailtash`, repository
  `pysv-const-expr-parser`, workflow `publish.yml`, and environment `pypi`.
  Configure that GitHub environment's deployment rules as appropriate.
- Connect the repository in Codecov; add `CODECOV_TOKEN` if required by the account.
- Import the repository into Read the Docs with slug `pysv-const-expr-parser`.
  `.readthedocs.yaml` installs the package and docs dependencies with uv and builds
  Sphinx on Python 3.14. Enable PR previews and released versions in Read the Docs
  as needed; Actions does not deploy the documentation.

Keep credentials out of committed files. Local editor and AI session state is
ignored; `AGENTS.md` is shared project guidance.
