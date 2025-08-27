"""
Configuration file for pytest.
This helps pytest discover tests properly in a Django project.
"""
import os

import django
import pytest
from django.conf import settings
from django.core.management import call_command

# Make Django settings accessible to pytest
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager.settings")
django.setup()


@pytest.fixture(scope="session")
def django_db_setup():
    """
    Fixture to set up the test database for Django tests.
    """
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
    # Apply migrations before running tests to create the database schema
    call_command('migrate')