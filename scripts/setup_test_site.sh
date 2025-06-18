#!/usr/bin/env bash
set -eo pipefail

SITE_NAME=${SITE_NAME:-test_site}
ADMIN_PWD=${ADMIN_PASSWORD:-admin}
BENCH_DIR="$HOME/ci-bench"

if [ ! -d "$BENCH_DIR" ]; then
  bench init "$BENCH_DIR" --skip-redis-config-generation --no-switch-bench
fi

cd "$BENCH_DIR"

if [ ! -d "sites/$SITE_NAME" ]; then
  bench new-site "$SITE_NAME" \
        --admin-password "$ADMIN_PWD" \
        --db-type sqlite \
        --no-mariadb-socket
  bench --site "$SITE_NAME" install-app ferum_customs
fi

cd "$OLDPWD"
ln -snf "$BENCH_DIR/sites/$SITE_NAME" "./test_site"
echo "✅ Site $SITE_NAME готов и смонтирован как ./test_site"
