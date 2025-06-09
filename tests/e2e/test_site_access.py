import pytest

# Skip test if 'requests' is not installed.
requests = pytest.importorskip("requests")


def test_site_index(frappe_site_container):
    resp = requests.get(frappe_site_container)
    assert resp.status_code == 200
