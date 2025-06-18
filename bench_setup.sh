#!/bin/bash
set -e

APP_NAME="ferum_customs"
SITE_NAME="${SITE_NAME:-dev.localhost}"
FRAPPE_BRANCH="${FRAPPE_BRANCH:-version-15}"
BENCH_DIR="${BENCH_DIR:-frappe-bench}"
APP_PATH="${APP_PATH:-$(pwd)/ferum_customs}"

init_bench() {
    if [ ! -d "$BENCH_DIR" ]; then
        bench init "$BENCH_DIR" --frappe-branch "$FRAPPE_BRANCH" --skip-assets
    fi
}

create_site() {
    if ! bench --site "$SITE_NAME" ls >/dev/null 2>&1; then
        DB_HOST="${DB_HOST:-mariadb}"
        DB_PORT="${DB_PORT:-3306}"
        DB_ROOT_USER="${DB_ROOT_USER:-root}"
        DB_ROOT_PASSWORD="${DB_ROOT_PASSWORD:-${MYSQL_ROOT_PASSWORD:-root}}"
        until mysqladmin ping -h"$DB_HOST" --silent; do
            echo "\u23F3 Waiting for MariaDB..."
            sleep 5
        done
        bench new-site "$SITE_NAME" \
            --admin-password "${ADMIN_PASSWORD:-admin}" \
            --db-host "$DB_HOST" \
            --db-port "$DB_PORT" \
            --mariadb-root-username "$DB_ROOT_USER" \
            --mariadb-root-password "$DB_ROOT_PASSWORD" \
            --no-mariadb-socket
    fi
}

install_app() {
    if ! bench list-apps | grep -q "$APP_NAME"; then
        bench get-app "$APP_NAME" --source_path "$APP_PATH"
        bench --site "$SITE_NAME" install-app "$APP_NAME"
    fi
}

case "$1" in
    tests)
        init_bench
        cd "$BENCH_DIR"
        create_site
        install_app
        bench --site "$SITE_NAME" run-tests --app "$APP_NAME" \
            --junit-xml="${JUNIT_XML:-/app/reports/bench-results.xml}"
        ;;
    dev|"" )
        init_bench
        cd "$BENCH_DIR"
        create_site
        install_app
        bench start
        ;;
    *)
        echo "Usage: $0 [dev|tests]"
        exit 1
        ;;
esac
