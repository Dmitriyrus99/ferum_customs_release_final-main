import pytest

try:
    import frappe  # noqa: F401
    from frappe.tests.utils import FrappeTestCase
except Exception:  # pragma: no cover - frappe not installed
    pytest.skip("frappe not available", allow_module_level=True)


class TestTestBasic(FrappeTestCase):
    def test_basic(self, frappe_site):
        self.assertTrue(True)
