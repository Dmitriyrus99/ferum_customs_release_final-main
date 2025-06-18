import os

import pytest

try:
    import frappe  # noqa: F401
    from frappe.tests.utils import FrappeTestCase
except Exception:  # pragma: no cover - frappe not installed
    pytest.skip("frappe not available", allow_module_level=True)


class TestTestBasic(FrappeTestCase):
    TEST_SITE = os.environ.get("SITE_NAME", getattr(frappe.local, "site", None))

    def test_basic(self, frappe_site):
        self.assertTrue(True)
