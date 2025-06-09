import requests


def test_site_running(frappe_site_container):
    resp = requests.get(frappe_site_container + "/api/method/ping")
    assert resp.status_code == 200
