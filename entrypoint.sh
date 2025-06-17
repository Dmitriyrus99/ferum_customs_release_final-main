#!/bin/bash
set -e

# Переходим в директорию стенда
cd /home/frappe/frappe-bench

# Создаем сайт и устанавливаем ERPNext
bench new-site test_site \
  --no-mariadb-socket \
  --admin-password 'admin' \
  --db-host mariadb \
  --db-port 3306 \
  --install-app erpnext

# Устанавливаем кастомное приложение
bench --site test_site install-app ferum_customs

# Запускаем сервис
bench start
