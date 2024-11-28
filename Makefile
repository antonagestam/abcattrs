SHELL := /usr/bin/env bash

.PHONY: clean
clean:
	rm -rf *.egg-info **/__pycache__ build dist

.PHONY: requirements
requirements: export CUSTOM_COMPILE_COMMAND='make requirements'
requirements:
	uv pip compile --extra=type-check --output-file=requirements-typing.txt pyproject.toml
