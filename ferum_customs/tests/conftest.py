import pytest
import os
import sys


@pytest.fixture(scope="session", autouse=True)
def setup_sys_path():
    """Ensure the ferum_customs module can be imported."""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if root not in sys.path:
        sys.path.insert(0, root)


@pytest.fixture(scope="session")
def site_host():
    """Provides base URL for frappe site."""
    return os.getenv("SITE_HOST", "http://localhost:8000")
