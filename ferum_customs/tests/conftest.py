import os
import sys

import frappe
import pytest

# Ensure package root is importable before tests are collected
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


@pytest.fixture(scope="session", autouse=True)
def setup_sys_path() -> None:
    """Ensure the :mod:`ferum_customs` module can be imported."""
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)


@pytest.fixture(scope="session")
def site_host() -> str:
    """Provides base URL for frappe site."""
    return os.getenv("SITE_HOST", "http://localhost:8000")


@pytest.fixture(scope="session", autouse=True)
def connect_site():
    """Connect to the already created Frappe site."""
    site = os.environ["SITE_NAME"]
    frappe.init(site)
    frappe.connect()
    yield
    frappe.destroy()
