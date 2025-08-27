#!/bin/bash
# Script to run tests and generate coverage and test reports for SonarQube

# Set environment variables for tests
export SECRET_KEY="test-secret-key-for-ci"
export DEBUG=True

# Run tests with coverage and generate XML report
python -m coverage run --source=task_manager --omit='*/migrations/*,*/settings.py,*/venv/*,*/.venv/*' -m pytest --junitxml=pytest-report.xml
python -m coverage xml

echo "Test and coverage reports generated successfully."