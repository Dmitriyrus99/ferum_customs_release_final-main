# Documentation Outline

## Architecture
- **API Layer (`ferum_customs/api.py`)** - whitelisted functions for Ajax calls and integrations.
- **Hooks (`ferum_customs/hooks.py` & `custom_hooks.py`)** - maps DocType events to logic in `custom_logic`.
- **Doctypes (`ferum_customs/doctype/`)** - service_request, ServiceReport, PayrollEntryCustom and others.
- **Custom Logic (`ferum_customs/custom_logic/`)** - validation and business rules used by hooks.
- **Permissions (`ferum_customs/permissions/`)** - dynamic permission filters.
- **Patches (`ferum_customs/patches/`)** - migration scripts applied with `bench migrate`.

## Data Flow
```
service_request --> ServiceReport --> PayrollEntryCustom
```
A service request is created and progressed through a workflow. Once work is completed, a ServiceReport is submitted and linked back to the request. PayrollEntryCustom records are created from approved reports.

## Roles & Permissions
| Role | Service Request | Service Report | Payroll Entry |
| ---- | --------------- | -------------- | ------------- |
| Проектный менеджер | full access | read | read |
| Инженер | read/write | create/submit | - |
| Заказчик | create/read own | - | - |

## User Guide
1. Войдите под своей учётной записью.
2. Создайте *Service Request* и заполните обязательные поля.
3. При необходимости приложите файлы (раздел Attachments).
4. После выполнения работ инженер отправляет *Service Report*.
5. Проектный менеджер проверяет отчёт и закрывает заявку.

## Developer Guide
1. Установите зависимости `pip install -r dev-requirements.txt`.
2. Запустите `bash bootstrap.sh` для создания сайта `dev.localhost`.
3. Запуск тестов и линтеров: `pre-commit run --all-files`.
4. Для применения патчей выполните `bench --site dev.localhost migrate`.
