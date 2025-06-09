#!/bin/bash
set -e

APP_NAME="ferum_customs"
SITE_NAME="${SITE_NAME:-dev.localhost}"
FRAPPE_BRANCH="${FRAPPE_BRANCH:-version-15}"
BENCH_DIR="${BENCH_DIR:-/home/frappe/frappe-bench}"
APP_PATH="$(cd "$(dirname "$0")" && pwd)"

if [ ! -d "$BENCH_DIR" ]; then
    sudo -u frappe -H bench init "$BENCH_DIR" --frappe-branch "$FRAPPE_BRANCH"
fi

cd "$BENCH_DIR"

if ! sudo -u frappe -H bench --site "$SITE_NAME" ls >/dev/null 2>&1; then
    sudo -u frappe -H bench new-site "$SITE_NAME" \
        --admin-password "${ADMIN_PASSWORD:-admin}" \
        --mariadb-root-password "${MYSQL_ROOT_PASSWORD:-root}"
fi

if ! sudo -u frappe -H bench list-apps | grep -q "$APP_NAME"; then
    sudo -u frappe -H bench get-app erpnext --branch "$FRAPPE_BRANCH"
    sudo -u frappe -H bench --site "$SITE_NAME" install-app erpnext
    sudo -u frappe -H bench get-app "$APP_NAME" --source-path "$APP_PATH"
    sudo -u frappe -H bench --site "$SITE_NAME" install-app "$APP_NAME"
fi

sudo -u frappe -H bench start
