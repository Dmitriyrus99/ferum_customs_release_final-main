# Ferum Customs – hooks
from .custom_hooks import DOC_EVENTS

app_name = "ferum_customs"
app_title = "Ferum Customs"
app_publisher = "Ferum LLC"
app_description = "Specific custom functionality for ERPNext"
app_email = "support@ferum.ru"
app_license = "MIT"

doc_events = DOC_EVENTS
get_notification_config = (
    "ferum_customs.notifications.notifications.get_notification_config"
)

# ── порядок фикстур: сначала DocType, затем поля/права, затем данные ──
fixtures = [
    "custom_fields.json",
    "custom_docperm.json",
    "workflow_service_request.json",
    "portal_menu_item.json",
    "notification.json",
    "role.json",
    "users.json",
    "customer.json",
]

try:                              # dev-hooks (если есть)
    from .dev_hooks import *      # noqa
except ImportError:
    pass
