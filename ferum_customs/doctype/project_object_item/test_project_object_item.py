import pytest

try:
    import frappe
    from frappe.tests.utils import FrappeTestCase
except Exception:  # pragma: no cover
    pytest.skip("frappe not available", allow_module_level=True)


class TestProjectObjectItem(FrappeTestCase):
    def test_description_trim(self, frappe_site):
        doc = frappe.new_doc("Project Object Item")
        doc.description = " Test description "
        doc.validate()
        self.assertEqual(doc.description, "Test description")
