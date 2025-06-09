import os
import subprocess
import shutil
import pytest

try:
    import frappe
except Exception:  # pragma: no cover - frappe not installed
    frappe = None


@pytest.fixture(scope="session")
def frappe_test_context():
    """
    Создает полноценный тестовый сайт Frappe один раз за сессию.
    """
    if frappe is None:
        pytest.skip("frappe not available")

    test_site_name = "test_site"
    cwd = os.getcwd()
    bench_cmd = shutil.which("bench")
    if bench_cmd is None:
        pytest.skip("bench CLI not available")
    bench_env = os.environ.copy()
    bench_env.setdefault("CI", "1")

    try:
        subprocess.run(
            [
                bench_cmd,
                "drop-site",
                test_site_name,
                "--force",
            ],
            check=False,
            env=bench_env,
        )
        try:
            subprocess.run(
                [
                    bench_cmd,
                    "new-site",
                    test_site_name,
                    "--admin-password",
                    "admin",
                    "--mariadb-root-password",
                    os.environ.get("MYSQL_ROOT_PASSWORD", "root"),
                ],
                check=True,
                env=bench_env,
            )
        except subprocess.CalledProcessError:
            pytest.skip("bench new-site failed")

        subprocess.run(
            [
                bench_cmd,
                "use",
                test_site_name,
            ],
            check=True,
            env=bench_env,
        )
        subprocess.run(
            [
                bench_cmd,
                "install-app",
                "erpnext",
            ],
            check=True,
            env=bench_env,
        )
        subprocess.run(
            [
                bench_cmd,
                "install-app",
                "ferum_customs",
            ],
            check=True,
            env=bench_env,
        )

        frappe.init(site=test_site_name)
        frappe.connect()
        frappe.flags.in_test = True

        yield

    finally:
        frappe.destroy()
        subprocess.run(
            [
                bench_cmd,
                "drop-site",
                test_site_name,
                "--force",
            ],
            check=False,
            env=bench_env,
        )
        os.chdir(cwd)


@pytest.fixture(autouse=True)
def use_frappe_test_context(frappe_test_context):
    yield
    frappe.db.rollback()


@pytest.fixture()
def frappe_site(frappe_test_context):
    return "test_site"
