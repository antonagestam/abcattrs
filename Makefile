SHELL := /usr/bin/env bash

.PHONY: clean
clean:
	rm -rf *.egg-info **/__pycache__ build dist
