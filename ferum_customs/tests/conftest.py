import os
import pathlib
import sys

import frappe
import pytest

# Ensure package root is importable before tests are collected
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

SITE = os.environ["SITE_NAME"]
SITE_PATH = pathlib.Path("test_site").resolve()


@pytest.fixture(scope="session", autouse=True)
def _connect():
    if not SITE_PATH.exists():
        pytest.fail(f"{SITE_PATH} not found – site preparation step failed")
    frappe.init(site=SITE, sites_path=str(SITE_PATH.parent))
    frappe.connect()
    yield
    frappe.destroy()
