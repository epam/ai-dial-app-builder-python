IMAGE_NAME ?= ai-dial-app-builder-python

.PHONY: all install build clean lint format

all: build

install:
	poetry install

build: install
	poetry build

clean:
	poetry env remove --all

lint: install
	poetry run nox -s lint

format: install
	poetry run nox -s format

help:
	@echo "===================="
	@echo "build                        - build the source and wheels archives"
	@echo "clean                        - clean virtual env and build artifacts"
	@echo "-- LINTING --"
	@echo "format                       - run code formatters"
	@echo "lint                         - run linters"
