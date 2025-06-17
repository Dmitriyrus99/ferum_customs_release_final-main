import pytest

pytest.importorskip("frappe")
from types import SimpleNamespace  # noqa: E402

import frappe  # noqa: E402
from frappe.tests.utils import FrappeTestCase  # noqa: E402

from ferum_customs import api  # noqa: E402


class DummyDoc(SimpleNamespace):
    def append(self, field, value):
        getattr(self, field).append(value)

    def insert(self, ignore_permissions=False):
        self.name = "INV-1"
        return self

    def get(self, key, default=None):
        return getattr(self, key, default)


class TestCreateInvoice(FrappeTestCase):
    def test_create_invoice_success(self, monkeypatch, frappe_site):
        sr = DummyDoc(
            name="SR-1",
            customer="Cust",
            work_items=[
                DummyDoc(description="Work", quantity=1, unit_price=10, amount=10)
            ],
        )
        invoice = DummyDoc(items=[])

        def fake_get_doc(*args, **kwargs):
            if isinstance(args[0], dict):
                invoice.customer = args[0].get("customer")
                invoice.service_report = args[0].get("service_report")
                return invoice
            if args[0] == "Service Report":
                return sr
            raise ValueError

        monkeypatch.setattr(frappe, "get_doc", fake_get_doc)
        monkeypatch.setattr(frappe.db, "exists", lambda *a, **k: False)
        monkeypatch.setattr(frappe, "has_permission", lambda *a, **k: True)

        name = api.create_invoice_from_report("SR-1")
        self.assertEqual(name, "INV-1")
        self.assertEqual(invoice.customer, sr.customer)
        self.assertEqual(invoice.service_report, "SR-1")
        self.assertEqual(invoice.items[0]["qty"], 1)

    def test_create_invoice_duplicate(self, monkeypatch, frappe_site):
        monkeypatch.setattr(frappe.db, "exists", lambda *a, **k: True)
        monkeypatch.setattr(
            frappe, "throw", lambda *a, **k: (_ for _ in ()).throw(Exception("throw"))
        )
        with pytest.raises(Exception):
            api.create_invoice_from_report("SR-1")
