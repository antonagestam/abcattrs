SHELL := /usr/bin/env bash

.PHONY: clean
clean:
	rm -rf *.egg-info **/__pycache__ build dist

.PHONY: requirements
requirements: export UV_CUSTOM_COMPILE_COMMAND='make requirements'
requirements:
	@uv pip compile \
		--extra=type-check \
		--generate-hashes \
		--strip-extras \
		--upgrade \
		--output-file=requirements-typing.txt \
		pyproject.toml
