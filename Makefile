SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help
MAKEFILE_DIR := $(patsubst %/,%,$(dir $(realpath $(firstword $(MAKEFILE_LIST)))))
PACKAGE_NAME := pysv-const-expr-parser
PACKAGE_VERSION ?= $(shell awk '/^version = / {gsub(/"/, "", $$3); print $$3; exit}' "$(MAKEFILE_DIR)/pyproject.toml")
WHEEL_DIR ?= $(MAKEFILE_DIR)/dist
UV ?= uv
TEST_ARGS ?=

.PHONY: help uv venv setup uv-lock uv-sync uv-sync-upgrade uv-list-outdated test coverage lint format format-python docs build test-wheel test-pypi test-testpypi cli vars
help: ## Show available commands
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "%-24s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
uv: ## Install uv
	curl -LsSf https://astral.sh/uv/install.sh | sh
venv: ## Create the Python 3.14 environment
	$(UV) venv --python 3.14
setup: uv-sync ## Synchronize all development dependencies
uv-lock: ## Refresh the dependency lockfile
	$(UV) lock
uv-sync: ## Sync all dependency groups from the lockfile
	$(UV) sync --locked --all-groups
uv-sync-upgrade: ## Upgrade locked dependencies and synchronize
	$(UV) lock --upgrade
	$(MAKE) uv-sync
uv-list-outdated: ## List outdated installed dependencies
	$(UV) pip list --outdated
test: ## Run SLY regression tests (optional TEST_ARGS)
	$(UV) run --locked pytest $(TEST_ARGS)
coverage: ## Run tests with terminal, XML, and HTML coverage
	$(UV) run --locked pytest $(TEST_ARGS) --cov --cov-report=term-missing --cov-report=xml:build/coverage/coverage.xml --cov-report=html:build/coverage/html
lint: ## Check Python lint and formatting
	$(UV) run --locked ruff check .
	$(UV) run --locked ruff format --check .
format: format-python ## Format first-party Python
format-python: ## Format first-party Python with Ruff
	$(UV) run --locked ruff format .
docs: ## Build Sphinx HTML with warnings treated as errors
	$(UV) run --locked sphinx-build -E -W -b html docs build/docs
build: ## Build wheel/source distributions and check metadata
	$(UV) build --out-dir "$(WHEEL_DIR)"
	$(UV) tool run --from twine twine check "$(WHEEL_DIR)"/*
test-wheel: ## Check installed wheel library and REPL outside the checkout
	@wheel=$$(find "$(WHEEL_DIR)" -maxdepth 1 -name 'pysv_const_expr_parser-$(PACKAGE_VERSION)-*.whl' -print -quit); \
	test -n "$$wheel" || { echo "No wheel for $(PACKAGE_VERSION) in $(WHEEL_DIR); run make build" >&2; exit 1; }; \
	wheel=$$(realpath "$$wheel"); \
	cd /tmp; \
	$(UV) run --no-project --python 3.14 --with "$$wheel" python "$(MAKEFILE_DIR)/tools/check_published.py" "$(PACKAGE_VERSION)"
test-pypi: ## Check a published PyPI release (override PACKAGE_VERSION)
	cd /tmp && $(UV) run --no-project --python 3.14 --refresh-package $(PACKAGE_NAME) --with '$(PACKAGE_NAME)==$(PACKAGE_VERSION)' python "$(MAKEFILE_DIR)/tools/check_published.py" "$(PACKAGE_VERSION)"
test-testpypi: ## Check a TestPyPI release (override PACKAGE_VERSION)
	cd /tmp && $(UV) run --no-project --python 3.14 --refresh-package $(PACKAGE_NAME) --index https://test.pypi.org/simple --index-strategy unsafe-best-match --with '$(PACKAGE_NAME)==$(PACKAGE_VERSION)' python "$(MAKEFILE_DIR)/tools/check_published.py" "$(PACKAGE_VERSION)"
cli: ## Start the SLY REPL
	$(UV) run --locked sv_expr_parser_repl
vars: ## Show package/build variables
	@printf '%s\n' 'MAKEFILE_DIR=$(MAKEFILE_DIR)' 'PACKAGE_NAME=$(PACKAGE_NAME)' 'PACKAGE_VERSION=$(PACKAGE_VERSION)' 'WHEEL_DIR=$(WHEEL_DIR)' 'UV=$(UV)'
var-%:
	@printf '%s\n' '$*=$($*)'
