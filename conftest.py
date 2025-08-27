"""
Configuration file for pytest.
This helps pytest discover tests properly in a Django project.
"""
import os

import django
import pytest

# Make Django settings accessible to pytest
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager.settings")
django.setup()