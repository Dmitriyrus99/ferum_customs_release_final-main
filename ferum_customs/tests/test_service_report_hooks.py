from types import SimpleNamespace
import pytest

try:
    import frappe
    from frappe.tests.utils import FrappeTestCase
except Exception:  # pragma: no cover - frappe not installed
    pytest.skip("frappe not available", allow_module_level=True)

from ferum_customs.custom_logic import service_report_hooks
from ferum_customs.constants import STATUS_VYPOLNENA


class DummyDoc(SimpleNamespace):
    def get(self, key):
        return getattr(self, key, None)


class TestServiceReportHooks(FrappeTestCase):
    def test_validate_ok(self, monkeypatch, frappe_site):
        doc = DummyDoc(service_request="REQ-1", name="SR-1")
        monkeypatch.setattr(frappe.db, "exists", lambda *a, **k: True)
        monkeypatch.setattr(frappe.db, "get_value", lambda *a, **k: STATUS_VYPOLNENA)
        service_report_hooks.validate(doc)

    def test_validate_missing_request(self, monkeypatch, frappe_site):
        doc = DummyDoc(service_request=None, name="SR-1")
        monkeypatch.setattr(
            frappe, "throw", lambda *a, **k: (_ for _ in ()).throw(Exception("throw"))
        )
        with pytest.raises(Exception):
            service_report_hooks.validate(doc)

    def test_validate_wrong_status(self, monkeypatch, frappe_site):
        doc = DummyDoc(service_request="REQ-1", name="SR-1")
        monkeypatch.setattr(frappe.db, "exists", lambda *a, **k: True)
        monkeypatch.setattr(frappe.db, "get_value", lambda *a, **k: "Открыта")
        monkeypatch.setattr(
            frappe, "throw", lambda *a, **k: (_ for _ in ()).throw(Exception("throw"))
        )
        with pytest.raises(Exception):
            service_report_hooks.validate(doc)
