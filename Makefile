.PHONY: lint format test clean install update fix-lint build publish test-publish coverage bump-patch bump-minor bump-major e2e-test e2e-test-mock

# Python version
PYTHON := python3

# Virtual environment
VENV := .venv
VENV_PYTHON := $(VENV)/bin/python

# Source directories
SRC_DIRS := .

# Default target
all: lint format test

# Linting
lint:
	@echo "Running ruff..."
	uv run ruff check $(SRC_DIRS)
	@echo "Running mypy..."
	uv run mypy $(SRC_DIRS)

# Fix linting errors
fix-lint:
	@echo "Fixing ruff errors..."
	uv run ruff check --fix $(SRC_DIRS)
	@echo "Running black..."
	uv run black $(SRC_DIRS)
	@echo "Running isort..."
	uv run isort $(SRC_DIRS)

# Formatting
format:
	@echo "Running black..."
	uv run black $(SRC_DIRS)
	@echo "Running isort..."
	uv run isort $(SRC_DIRS)

# Testing
test:
	@echo "Running tests..."
	uv run pytest

# Coverage
coverage:
	@echo "Running tests with coverage..."
	uv run pytest --cov=web3_mcp --cov-report=term --cov-report=xml --cov-report=html

# Clean up
clean:
	@echo "Cleaning up..."
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ *.egg-info/ htmlcov/ .coverage coverage.xml

# Install dependencies
install:
	@echo "Installing dependencies..."
	uv pip install -e ".[dev]"

# Update dependencies
update:
	@echo "Updating dependencies..."
	uv pip install --upgrade -e ".[dev]"

# Build package
build: clean
	@echo "Building package..."
	uv run python -m build

# Test publish to TestPyPI
test-publish: build
	@echo "Publishing to TestPyPI..."
	uv run twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# Publish to PyPI
publish: build
	@echo "Publishing to PyPI..."
	uv run twine upload dist/*

# Version bumping
VERSION_FILE := src/web3_mcp/__version__.py

# Helper function to update version
define update_version
	@echo "Updating version to $(1)"
	@sed -i.bak 's/__version__ = "[^"]*"/__version__ = "$(1)"/' $(VERSION_FILE)
	@rm -f $(VERSION_FILE).bak
	@git add $(VERSION_FILE)
	@git commit -m "Bump version to $(1)"
	@git tag -a v$(1) -m "Version $(1)"
	@echo "Version updated to $(1). Don't forget to push with: git push && git push --tags"
endef

# Get current version (macOS compatible)
CURRENT_VERSION := $(shell grep -o '"[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*[^"]*"' $(VERSION_FILE) | tr -d '"')
VERSION_BASE := $(shell echo $(CURRENT_VERSION) | sed -E 's/([0-9]+\.[0-9]+\.[0-9]+).*/\1/')
VERSION_SUFFIX := $(shell echo $(CURRENT_VERSION) | grep -o -- "-[a-zA-Z0-9]\+" || echo "")
MAJOR := $(shell echo $(VERSION_BASE) | cut -d. -f1)
MINOR := $(shell echo $(VERSION_BASE) | cut -d. -f2)
PATCH := $(shell echo $(VERSION_BASE) | cut -d. -f3)

# Bump patch version (0.0.x)
bump-patch:
	@current_version=$$(grep -o '__version__ = ".*"' $(VERSION_FILE) | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+'); \
	IFS='.' read -r major minor patch <<< "$$current_version"; \
	new_patch=$$((patch + 1)); \
	new_version="$$major.$$minor.$$new_patch"; \
	echo "Updating version to $$new_version"; \
	sed -i '' "s/__version__ = \".*\"/__version__ = \"$$new_version\"/" $(VERSION_FILE); \
	git add $(VERSION_FILE); \
	git commit -m "Bump version to $$new_version"; \
	git tag -a v$$new_version -m "Version $$new_version"; \
	echo "Version updated to $$new_version. Don't forget to push with: git push && git push --tags"

# Bump minor version (0.x.0)
bump-minor:
	@current_version=$$(grep -o '__version__ = ".*"' $(VERSION_FILE) | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+'); \
	IFS='.' read -r major minor patch <<< "$$current_version"; \
	new_minor=$$((minor + 1)); \
	new_version="$$major.$$new_minor.0"; \
	echo "Updating version to $$new_version"; \
	sed -i '' "s/__version__ = \".*\"/__version__ = \"$$new_version\"/" $(VERSION_FILE); \
	git add $(VERSION_FILE); \
	git commit -m "Bump version to $$new_version"; \
	git tag -a v$$new_version -m "Version $$new_version"; \
	echo "Version updated to $$new_version. Don't forget to push with: git push && git push --tags"

# Bump major version (x.0.0)
bump-major:
	@current_version=$$(grep -o '__version__ = ".*"' $(VERSION_FILE) | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+'); \
	IFS='.' read -r major minor patch <<< "$$current_version"; \
	new_major=$$((major + 1)); \
	new_version="$$new_major.0.0"; \
	echo "Updating version to $$new_version"; \
	sed -i '' "s/__version__ = \".*\"/__version__ = \"$$new_version\"/" $(VERSION_FILE); \
	git add $(VERSION_FILE); \
	git commit -m "Bump version to $$new_version"; \
	git tag -a v$$new_version -m "Version $$new_version"; \
	echo "Version updated to $$new_version. Don't forget to push with: git push && git push --tags"

# Bump beta version (x.x.x-beta)
bump-beta:
	$(eval NEW_VERSION := $(VERSION_BASE)-beta)
	$(call update_version,$(NEW_VERSION))

# E2E Testing
e2e-test:
	uv run python -m pytest e2e_tests -v

e2e-test-mock:
	uv run python -m pytest e2e_tests/test_mock.py -v

# Push version changes and tags
push-version:
	git push && git push --tags
