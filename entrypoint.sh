#!/bin/bash
set -e

BENCH_FOLDER="${BENCH_FOLDER:-frappe-bench}"
SITE_NAME="${SITE_NAME:-test_site}"
ADMIN_PWD="${ADMIN_PWD:-admin}"
DB_ROOT_PWD="${DB_ROOT_PWD:-""}"

if [ ! -d "$BENCH_FOLDER" ]; then
    /bootstrap.sh
fi

cd "$BENCH_FOLDER"

if [ ! -f "/home/frappe/frappe-bench/sites/${SITE_NAME}/site_config.json" ]; then
    echo ">> Creating Frappe site ${SITE_NAME}"
    bench new-site "$SITE_NAME" \
         --admin-password "$ADMIN_PWD" \
         --mariadb-root-password "$DB_ROOT_PWD" \
         --install-app erpnext
fi

bench use "$SITE_NAME"

if [[ "$1" == "pytest" ]]; then
    shift
    bench --site "$SITE_NAME" run-tests --app ferum_customs \
        --junit-xml="${JUNIT_XML:-/app/reports/bench-results.xml}" "$@"
else
    exec "$@"
fi
