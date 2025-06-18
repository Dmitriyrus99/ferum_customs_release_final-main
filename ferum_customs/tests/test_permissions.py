import os

import pytest

try:
    import frappe
    from frappe.tests.utils import FrappeTestCase
except Exception:  # pragma: no cover
    pytest.skip("frappe not available", allow_module_level=True)


class TestPermissions(FrappeTestCase):
    TEST_SITE = os.environ.get("SITE_NAME", getattr(frappe.local, "site", None))

    def test_sales_user_cannot_cancel(self, frappe_site):
        sr = frappe.new_doc("Service Request")
        sr.subject = "Perm Test"
        sr.status = "Открыта"
        sr.insert(ignore_permissions=True)
        sr.submit()

        user = frappe.get_doc(
            {
                "doctype": "User",
                "email": "sales@example.com",
                "first_name": "Sales",
                "roles": [{"role": "Sales User"}],
            }
        )
        user.insert(ignore_permissions=True)

        frappe.set_user(user.name)
        with pytest.raises(frappe.PermissionError):
            sr.cancel()

        frappe.set_user("Administrator")
