from types import SimpleNamespace

import pytest

try:
    import frappe
    from frappe.tests.utils import FrappeTestCase
except Exception:  # pragma: no cover - frappe not installed
    pytest.skip("frappe not available", allow_module_level=True)

from ferum_customs.custom_logic import service_request_hooks


class DummyEntry(SimpleNamespace):
    def get(self, key):
        return getattr(self, key, None)


class TestServiceRequestHooks(FrappeTestCase):
    def test_get_engineers(self, monkeypatch, frappe_site):
        doc = SimpleNamespace(
            assigned_engineers=[
                DummyEntry(engineer="u1"),
                DummyEntry(engineer="u1"),
                DummyEntry(engineer="u2"),
            ]
        )
        monkeypatch.setattr(frappe, "get_doc", lambda *a, **k: doc)
        result = service_request_hooks.get_engineers_for_object("OBJ")
        self.assertEqual(set(result), {"u1", "u2"})

    def test_get_engineers_missing(self, monkeypatch, frappe_site):
        class DoesNotExist(Exception):
            pass

        monkeypatch.setattr(
            service_request_hooks.frappe,
            "DoesNotExistError",
            DoesNotExist,
            raising=False,
        )

        def raise_missing(*a, **k):
            raise DoesNotExist

        monkeypatch.setattr(frappe, "get_doc", raise_missing)
        result = service_request_hooks.get_engineers_for_object("OBJ")
        self.assertEqual(result, [])
