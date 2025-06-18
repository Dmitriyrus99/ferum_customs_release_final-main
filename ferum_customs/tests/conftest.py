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
def init_frappe_site():
    """Initialize and connect to the Frappe site for the test session."""
    site = os.environ.get("SITE_NAME") or getattr(frappe.local, "site", None)
    if not site:
        pytest.skip("No Frappe site available")
    frappe.init(site)
    frappe.connect()
    yield
    frappe.destroy()
