"""
Configuration file for pytest.
This helps pytest discover tests properly in a Django project.
"""
import os

import django

# Make Django settings accessible to pytest
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager.settings")
# Set a default SECRET_KEY for tests if not already set
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest")
os.environ.setdefault("DEBUG", "True")

django.setup()