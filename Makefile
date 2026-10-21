.DEFAULT_GOAL := help
.PHONY: help setup test coverage lint format docs build cli
help:
	@echo "Targets: setup test coverage lint format docs build cli"
setup:
	uv sync --locked --all-groups
test:
	uv run --locked pytest
coverage:
	uv run --locked pytest --cov --cov-report=term-missing --cov-report=xml:build/coverage/coverage.xml --cov-report=html:build/coverage/html
lint:
	uv run --locked ruff check .
	uv run --locked ruff format --check .
format:
	uv run --locked ruff format .
docs:
	uv run --locked sphinx-build -E -W -b html docs build/docs
build:
	uv build
	uv tool run --from twine twine check dist/*
cli:
	uv run --locked sv_expr_parser_repl
