MAKEFILE_DIR   = $(patsubst %/,%,$(dir $(realpath $(firstword $(MAKEFILE_LIST)))))

-include $(MAKEFILE_DIR)/Makefile-helper.mk

# Keep recipes fail-fast and preserve failures in pipelines.
SHELL          := /bin/bash
.SHELLFLAGS    := -eu -o pipefail -c
.DEFAULT_GOAL  := help

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

UV             ?= uv
PACKAGE_NAME   := pysv-const-expr-parser

# Published-package smoke checks default to the version declared in pyproject.toml.
# Select another release with: make test-testpypi PACKAGE_VERSION=0.2.1
PACKAGE_VERSION ?= $(shell awk '/^version = / {gsub(/"/, "", $$3); print $$3; exit}' "$(MAKEFILE_DIR)/pyproject.toml")

# Build and smoke-check another output directory with: make build test-wheel WHEEL_DIR=dist/0.1.0
WHEEL_DIR      ?= $(MAKEFILE_DIR)/dist

# Select regression tests with: make test TEST_ARGS="-k evaluation"
TEST_ARGS      ?=

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##@ Setup:
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ----------------------------------------------------------------------------------------------------------------------
# setup: ## Synchronize all development dependencies
# ----------------------------------------------------------------------------------------------------------------------
.PHONY: setup
setup: uv-sync


# ----------------------------------------------------------------------------------------------------------------------
# uv: ## Install uv
# ----------------------------------------------------------------------------------------------------------------------
.PHONY: uv
uv:
	curl -LsSf https://astral.sh/uv/install.sh | sh

# ----------------------------------------------------------------------------------------------------------------------
# venv: ## Create the Python 3.14 environment
# ----------------------------------------------------------------------------------------------------------------------
.PHONY: venv
venv:
	$(UV) venv --python 3.14

# ----------------------------------------------------------------------------------------------------------------------
# uv-lock: ## Refresh the dependency lockfile
# ----------------------------------------------------------------------------------------------------------------------
.PHONY: uv-lock
uv-lock:
	$(UV) lock

# ----------------------------------------------------------------------------------------------------------------------
# uv-sync: ## Sync all dependency groups from the lockfile
# ----------------------------------------------------------------------------------------------------------------------
.PHONY: uv-sync
uv-sync:
	$(UV) sync --locked --all-groups

# ----------------------------------------------------------------------------------------------------------------------
# uv-sync-upgrade: ## Upgrade locked dependencies and synchronize
# ----------------------------------------------------------------------------------------------------------------------
.PHONY: uv-sync-upgrade
uv-sync-upgrade:
	$(UV) lock --upgrade
	$(MAKE) uv-sync

# ----------------------------------------------------------------------------------------------------------------------
# uv-list-outdated: ## List outdated installed dependencies
# ----------------------------------------------------------------------------------------------------------------------
.PHONY: uv-list-outdated
uv-list-outdated:
	$(UV) pip list --outdated

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##@ Build and validation:
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ----------------------------------------------------------------------------------------------------------------------
# build: ## Build wheel/source distributions and check metadata
# ----------------------------------------------------------------------------------------------------------------------
.PHONY: build
build:
	$(UV) build --out-dir "$(WHEEL_DIR)"
	$(UV) tool run --from twine twine check "$(WHEEL_DIR)"/*

# ----------------------------------------------------------------------------------------------------------------------
# test: ## Run SLY regression tests (optional TEST_ARGS)
# ----------------------------------------------------------------------------------------------------------------------
.PHONY: test
test:
	$(UV) run --locked pytest $(TEST_ARGS)

# ----------------------------------------------------------------------------------------------------------------------
# lint: ## Check Python lint and formatting
# ----------------------------------------------------------------------------------------------------------------------
.PHONY: lint
lint:
	$(UV) run --locked ruff check .
	$(UV) run --locked ruff format --check .

# ----------------------------------------------------------------------------------------------------------------------
# format-python: ## Format first-party Python with Ruff
# ----------------------------------------------------------------------------------------------------------------------
.PHONY: format-python
format-python:
	$(UV) run --locked ruff format .

# ----------------------------------------------------------------------------------------------------------------------
# format: ## Format first-party Python
# ----------------------------------------------------------------------------------------------------------------------
.PHONY: format
format: format-python


# ----------------------------------------------------------------------------------------------------------------------
# coverage: ## Run tests with terminal, XML, and HTML coverage
# ----------------------------------------------------------------------------------------------------------------------
.PHONY: coverage
coverage:
	$(UV) run --locked pytest $(TEST_ARGS) --cov --cov-report=term-missing --cov-report=xml:build/coverage/coverage.xml --cov-report=html:build/coverage/html

# ----------------------------------------------------------------------------------------------------------------------
# test-wheel: ## Check installed wheel library and REPL outside the checkout
# ----------------------------------------------------------------------------------------------------------------------
.PHONY: test-wheel
test-wheel:
	@wheel=$$(find "$(WHEEL_DIR)" -maxdepth 1 -name 'pysv_const_expr_parser-$(PACKAGE_VERSION)-*.whl' -print -quit); \
	test -n "$$wheel" || { echo "No wheel for $(PACKAGE_VERSION) in $(WHEEL_DIR); run make build" >&2; exit 1; }; \
	wheel=$$(realpath "$$wheel"); \
	cd /tmp; \
	$(UV) run --no-project --python 3.14 --with "$$wheel" python "$(MAKEFILE_DIR)/tools/check_published.py" "$(PACKAGE_VERSION)"

# ----------------------------------------------------------------------------------------------------------------------
# test-testpypi: ## Check a TestPyPI release (override PACKAGE_VERSION)
# ----------------------------------------------------------------------------------------------------------------------
.PHONY: test-testpypi
test-testpypi:
	cd /tmp && $(UV) run --no-project --python 3.14 --refresh-package $(PACKAGE_NAME) --index https://test.pypi.org/simple --index-strategy unsafe-best-match --with '$(PACKAGE_NAME)==$(PACKAGE_VERSION)' python "$(MAKEFILE_DIR)/tools/check_published.py" "$(PACKAGE_VERSION)"

# ----------------------------------------------------------------------------------------------------------------------
# test-pypi: ## Check a published PyPI release (override PACKAGE_VERSION)
# ----------------------------------------------------------------------------------------------------------------------
.PHONY: test-pypi
test-pypi:
	cd /tmp && $(UV) run --no-project --python 3.14 --refresh-package $(PACKAGE_NAME) --with '$(PACKAGE_NAME)==$(PACKAGE_VERSION)' python "$(MAKEFILE_DIR)/tools/check_published.py" "$(PACKAGE_VERSION)"

# ----------------------------------------------------------------------------------------------------------------------
# docs: ## Build Sphinx HTML with warnings treated as errors
# ----------------------------------------------------------------------------------------------------------------------
.PHONY: docs
docs:
	$(UV) run --locked sphinx-build -E -W -b html docs build/docs

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##@ Interpreter:
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ----------------------------------------------------------------------------------------------------------------------
# cli: ## Start the SLY REPL
# ----------------------------------------------------------------------------------------------------------------------
.PHONY: cli
cli:
	$(UV) run --locked sv_expr_parser_repl

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##@ General:
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ----------------------------------------------------------------------------------------------------------------------
# vars: ## Show package/build variables
# ----------------------------------------------------------------------------------------------------------------------
.PHONY: vars
vars:
	@printf '%s\n' 'MAKEFILE_DIR=$(MAKEFILE_DIR)' 'PACKAGE_NAME=$(PACKAGE_NAME)' 'PACKAGE_VERSION=$(PACKAGE_VERSION)' 'WHEEL_DIR=$(WHEEL_DIR)' 'UV=$(UV)'

# ----------------------------------------------------------------------------------------------------------------------
# var-<VARIABLE>: ## Print a single Makefile variable
# ----------------------------------------------------------------------------------------------------------------------
var-%:
	@printf '%s\n' '$*=$($*)'
