import sys
import types
from types import SimpleNamespace
from pathlib import Path
from typing import Any, cast
import importlib
import pytest

# Ensure project root is on sys.path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ferum_customs import constants


def make_frappe(tmp_path: Path):
    """Create a minimal stub of the frappe module for tests."""
    frappe = cast(Any, types.ModuleType("frappe"))

    class DummyLogger:
        def __init__(self, name=None):
            self.name = name
            self.messages = []

        def warning(self, msg, *a, **k):
            self.messages.append(("warning", msg))

        def info(self, msg, *a, **k):
            self.messages.append(("info", msg))

        def error(self, msg, *a, **k):
            self.messages.append(("error", msg))

    frappe.logger = lambda name=None: DummyLogger(name)
    frappe._ = lambda x: x
    frappe.throw = lambda msg, *a, **k: (_ for _ in ()).throw(Exception(msg))
    frappe.msgprint = lambda *a, **k: None
    frappe.sendmail = lambda **k: None
    frappe.get_all = lambda *a, **k: []
    frappe.get_cached_value = lambda *a, **k: None
    frappe.delete_doc = lambda *a, **k: None

    frappe.session = SimpleNamespace(user="test-user")

    class DB:
        def __init__(self):
            self.get_value = lambda *a, **k: None
            self.exists = lambda *a, **k: None

    frappe.db = DB()

    frappe.flags = {}

    class Utils:
        def __init__(self, base: Path):
            self.base = base

        def now(self):
            return "NOW"

        def get_link_to_form(self, doctype: str, name: str) -> str:
            return f"/{doctype}/{name}"

    utils = Utils(tmp_path)
    frappe.utils = utils

    def get_site_path(*parts):
        return str(tmp_path.joinpath(*parts))

    frappe.get_site_path = get_site_path
    frappe.whitelist = lambda *d, **kw: (lambda func: func)
    frappe.generate_hash = lambda: "hash"
    frappe.DoesNotExistError = type("DoesNotExistError", (Exception,), {})
    return frappe


@pytest.fixture()
def frappe_stub(monkeypatch, tmp_path):
    frappe = make_frappe(tmp_path)
    sys.modules["frappe"] = frappe
    sys.modules["frappe.utils"] = frappe.utils
    yield frappe
    sys.modules.pop("frappe", None)
    sys.modules.pop("frappe.utils", None)


class DummyDoc:
    def __init__(self, **kwargs):
        self.name = None
        self.__dict__.update(kwargs)
        self.meta = SimpleNamespace(has_field=lambda f: True)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def set(self, key, value):
        setattr(self, key, value)


def test_validate_requires_linked_report(frappe_stub):
    hooks = importlib.reload(
        importlib.import_module("ferum_customs.custom_logic.service_request_hooks")
    )
    doc = DummyDoc(
        status=constants.STATUS_VYPOLNENA, custom_linked_report=None, name="SR1"
    )
    with pytest.raises(Exception):
        hooks.validate(doc)


def test_validate_sets_completed_on(frappe_stub):
    hooks = importlib.reload(
        importlib.import_module("ferum_customs.custom_logic.service_request_hooks")
    )
    doc = DummyDoc(
        status=constants.STATUS_VYPOLNENA,
        custom_linked_report="REP",
        completed_on=None,
        name="SR1",
    )
    hooks.validate(doc)
    assert doc.completed_on == "NOW"


def test_validate_project_autofill(frappe_stub):
    hooks = importlib.reload(
        importlib.import_module("ferum_customs.custom_logic.service_request_hooks")
    )
    frappe_stub.db.get_value = lambda *a, **k: "CUST1"
    doc = DummyDoc(
        status="", custom_linked_report="REP", custom_project="PRJ", name="SR1"
    )
    hooks.validate(doc)
    assert doc.custom_customer == "CUST1"


def test_validate_project_missing_customer(frappe_stub):
    hooks = importlib.reload(
        importlib.import_module("ferum_customs.custom_logic.service_request_hooks")
    )
    frappe_stub.db.get_value = lambda *a, **k: None
    doc = DummyDoc(
        status="", custom_linked_report="REP", custom_project="PRJ", name="SR1"
    )
    with pytest.raises(Exception):
        hooks.validate(doc)


def test_prevent_deletion_with_links(frappe_stub):
    hooks = importlib.reload(
        importlib.import_module("ferum_customs.custom_logic.service_request_hooks")
    )
    frappe_stub.db.exists = lambda *a, **k: "REP1"
    doc = DummyDoc(name="SR1")
    with pytest.raises(Exception):
        hooks.prevent_deletion_with_links(doc)


def test_delete_attachment_file(frappe_stub, tmp_path):
    utils_mod = importlib.reload(
        importlib.import_module("ferum_customs.custom_logic.file_attachment_utils")
    )
    base = Path(frappe_stub.get_site_path("public", "files"))
    base.mkdir(parents=True, exist_ok=True)
    file_path = base / "f.txt"
    file_path.write_text("hi")
    utils_mod.delete_attachment_file_from_filesystem("/files/f.txt")
    assert not file_path.exists()


def test_delete_attachment_bad_url(frappe_stub):
    utils_mod = importlib.reload(
        importlib.import_module("ferum_customs.custom_logic.file_attachment_utils")
    )
    with pytest.raises(Exception):
        utils_mod.delete_attachment_file_from_filesystem("/files/../hack")


def test_payroll_entry_validate_dates(frappe_stub):
    hooks = importlib.reload(
        importlib.import_module("ferum_customs.custom_logic.payroll_entry_hooks")
    )
    doc = DummyDoc(start_date=2, end_date=1)
    with pytest.raises(Exception):
        hooks.validate(doc)


def test_payroll_entry_before_save_default(frappe_stub):
    hooks = importlib.reload(
        importlib.import_module("ferum_customs.custom_logic.payroll_entry_hooks")
    )
    doc = DummyDoc(total_payable=None)
    hooks.before_save(doc)
    assert doc.total_payable == 0.0
