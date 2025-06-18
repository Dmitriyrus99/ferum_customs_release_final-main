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
BENCH_DIR = pathlib.Path(".bench")


@pytest.fixture(scope="session", autouse=True)
def connect_frappe():
    site_path = BENCH_DIR / "sites" / SITE
    if not site_path.exists():
        pytest.skip(f"Site {SITE} not found, run setup_test_site.sh")
    frappe.init(site=SITE, sites_path=str(BENCH_DIR / "sites"))
    frappe.connect()
    yield
    frappe.destroy()
