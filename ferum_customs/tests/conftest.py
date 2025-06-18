import os
import pathlib
import sys

import pytest

frappe = pytest.importorskip("frappe")

# Ensure package root is importable before tests are collected
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

SITE = os.environ.get("SITE_NAME", "test_site")
SITES_PATH = pathlib.Path(os.environ.get("SITES_PATH", ".bench/sites"))


@pytest.fixture(scope="session", autouse=True)
def connect_frappe():
    # если Frappe уже подключён сайтом из FrappeTestCase, ничего не делаем
    if getattr(frappe.local, "site", None) == SITE:
        return

    site_path = SITES_PATH / SITE
    if not site_path.exists():
        pytest.skip(f"Site {site_path} not found – run setup_test_site.sh")

    frappe.init(site=SITE, sites_path=str(SITES_PATH))
    frappe.connect()
    yield
    frappe.destroy()
