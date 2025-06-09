#!/bin/bash
set -e

APP_NAME="ferum_customs"
SITE_NAME="${SITE_NAME:-dev.localhost}"
APP_PATH="/app/ferum_customs"
FRAPPE_BRANCH="${FRAPPE_BRANCH:-version-15}"

# Initialize bench if folder does not exist
if [ ! -d frappe-bench ]; then
    echo "[bootstrap] Initializing bench..."
    bench init frappe-bench --frappe-branch "$FRAPPE_BRANCH" --skip-assets
fi

cd frappe-bench

if ! bench --site "$SITE_NAME" ls >/dev/null 2>&1; then
    echo "[bootstrap] Creating site $SITE_NAME..."
    bench new-site "$SITE_NAME" \
        --admin-password "${ADMIN_PASSWORD:-admin}" \
        --mariadb-root-password "${MYSQL_ROOT_PASSWORD:-root}"

    echo "[bootstrap] Installing app from $APP_PATH..."
    bench get-app "$APP_NAME" --source-path "$APP_PATH"
    bench --site "$SITE_NAME" install-app "$APP_NAME"
fi

echo "[bootstrap] Running tests for $APP_NAME..."
bench --site "$SITE_NAME" run-tests --app "$APP_NAME" \
    --junit-xml="${JUNIT_XML:-/app/reports/bootstrap-results.xml}"
