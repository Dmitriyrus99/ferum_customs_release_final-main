#!/usr/bin/env bash
set -euo pipefail

export CI=${CI:-true}

SITE_NAME=${SITE_NAME:-test_site}
ADMIN_PWD=${ADMIN_PASSWORD:-admin}

# Создать bench в каталоге .bench, если ещё нет
if [ ! -d ".bench" ]; then
  bench init .bench --skip-assets --skip-redis-config-generation
fi

cd .bench

# Создать сайт ― пропускаем, если уже создан
if [ ! -d "sites/$SITE_NAME" ]; then
  bench new-site "$SITE_NAME" \
        --admin-password "$ADMIN_PWD" \
        --db-type sqlite \
        --no-mariadb-socket
fi

# Установить ваши приложения (и ERPNext при необходимости)
bench --site "$SITE_NAME" install-app ferum_customs
# bench --site "$SITE_NAME" install-app erpnext   # если нужно

# Создать символическую ссылку ../test_site → .bench/sites/test_site
SITE_PATH="sites/$SITE_NAME"
BENCH_DIR=".bench"
if [ ! -e "../test_site" ]; then
  ln -s "$SITE_PATH" ../test_site
fi
echo "✅ Symlink ../test_site → $BENCH_DIR/$SITE_PATH готов"

echo "✅ Site $SITE_NAME ready"
