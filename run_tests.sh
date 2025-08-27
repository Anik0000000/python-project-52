#!/bin/bash
# Script to run tests and generate coverage and test reports for SonarQube

# Set environment variables for tests if not already set
SECRET_KEY=${SECRET_KEY:-"test-secret-key-for-ci"}
export SECRET_KEY

DEBUG=${DEBUG:-True}
export DEBUG

echo "Installing dev dependencies..."
uv sync --group dev

echo "Running tests with coverage reporting..."

# Run tests with coverage and generate XML report
uv run -m coverage run --source=task_manager --omit='*/migrations/*,*/settings.py,*/venv/*,*/.venv/*' -m pytest --junitxml=pytest-report.xml

# Generate coverage report in XML format for SonarQube
uv run -m coverage xml

echo "Test and coverage reports generated successfully."