import os
import pathlib
import subprocess
import sys

import pytest

frappe = pytest.importorskip("frappe")

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
def ensure_test_site(tmp_path_factory):
    site = os.environ.get("SITE_NAME", "test_site")
    bench_path = pathlib.Path(".bench")
    sites_dir = bench_path / "sites"

    if not (sites_dir / site).exists():
        subprocess.check_call(
            [
                "bench",
                "init",
                str(bench_path),
                "--skip-redis-config-generation",
            ]
        )
        subprocess.check_call(
            [
                "bench",
                "--site",
                site,
                "new-site",
                "--db-type",
                "sqlite",
                "--admin-password",
                "admin",
                "--db-name",
                f"{site}.db",
            ]
        )
        subprocess.check_call(
            [
                "bench",
                "--site",
                site,
                "install-app",
                "ferum_customs",
            ]
        )

    frappe.init(site)
    frappe.connect()
    yield
    frappe.destroy()
