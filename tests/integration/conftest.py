import shutil
import subprocess
import time

import pytest

# Skip the integration tests early when the 'requests' package is not available.
requests = pytest.importorskip("requests")


def _wait_for_site(url: str, timeout: int = 120) -> None:
    for _ in range(timeout):
        try:
            requests.get(url, timeout=5)
            return
        except requests.RequestException:
            time.sleep(1)
    raise RuntimeError("Site did not start")


@pytest.fixture(scope="session")
def frappe_site_container():
    if shutil.which("docker") is None:
        pytest.skip("docker not available")
    subprocess.check_call(
        ["docker", "compose", "-f", "docker-compose.yml", "up", "-d", "--build"]
    )
    try:
        _wait_for_site("http://localhost:8000/api/method/ping")
        yield "http://localhost:8000"
    finally:
        subprocess.call(["docker", "compose", "-f", "docker-compose.yml", "down", "-v"])
