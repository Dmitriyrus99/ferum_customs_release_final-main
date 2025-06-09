# ferum_customs/tests/conftest.py

import pytest
import os
import sys

@pytest.fixture(scope="session", autouse=True)
def setup_sys_path():
    """Ensure the ferum_customs module can be imported."""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if root not in sys.path:
        sys.path.insert(0, root)

@pytest.fixture(scope="session")
def site_host():
    """Provides base URL for frappe site."""
    return os.getenv("SITE_HOST", "http://localhost:8000")

# ferum_customs/tests/test_example.py

import pytest
import requests


def test_sample():
    assert 1 + 1 == 2


def test_import():
    try:
        import ferum_customs
    except ImportError:
        pytest.fail("ferum_customs package could not be imported")


def test_business_logic_validate_data():
    from ferum_customs.custom_logic import service_report_hooks

    sample_data = {
        "report_type": "inspection",
        "status": "open",
    }

    result = service_report_hooks.validate_data(sample_data)
    assert result is True


def test_business_logic_missing_field():
    from ferum_customs.custom_logic import service_report_hooks

    sample_data = {
        "status": "open",
    }

    with pytest.raises(KeyError):
        service_report_hooks.validate_data(sample_data)


def test_ping_endpoint(site_host):
    """Check if the Frappe instance is running."""
    try:
        response = requests.get(f"{site_host}/api/method/ping")
        assert response.status_code == 200
        assert response.json().get("message") == "pong"
    except requests.exceptions.ConnectionError:
        pytest.skip("Frappe instance not reachable.")


def test_post_get_current_user(site_host):
    """Test a real frappe method: common.get_logged_user."""
    try:
        response = requests.post(
            f"{site_host}/api/method/frappe.auth.get_logged_user"
        )
        assert response.status_code == 200
        json_data = response.json()
        assert "message" in json_data
        assert isinstance(json_data["message"], str)
    except requests.exceptions.ConnectionError:
        pytest.skip("Frappe instance not reachable.")


def test_post_logout(site_host):
    """Test frappe.auth.logout to terminate session."""
    try:
        response = requests.post(f"{site_host}/api/method/frappe.auth.logout")
        assert response.status_code == 200
        json_data = response.json()
        assert json_data.get("message") == "Logged out"
    except requests.exceptions.ConnectionError:
        pytest.skip("Frappe instance not reachable.")
