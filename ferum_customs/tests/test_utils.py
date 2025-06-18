import os

import pytest

pytest.importorskip("frappe")
from types import SimpleNamespace  # noqa: E402

import frappe  # noqa: E402
from frappe.tests.utils import FrappeTestCase  # noqa: E402

from ferum_customs.custom_logic import service_request_hooks  # noqa: E402


class DummyEntry(SimpleNamespace):
    def get(self, key):
        return getattr(self, key, None)


class TestUtils(FrappeTestCase):
    TEST_SITE = os.environ.get("SITE_NAME", getattr(frappe.local, "site", None))

    def test_get_engineers_for_object(self, monkeypatch, frappe_site):
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
