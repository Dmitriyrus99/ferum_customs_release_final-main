#!/bin/bash
set -e

APP_NAME="ferum_customs"
SITE_NAME="${SITE_NAME:-dev.localhost}"
FRAPPE_BRANCH="${FRAPPE_BRANCH:-version-15}"
BENCH_DIR="${BENCH_DIR:-/home/frappe/frappe-bench}"
APP_PATH="$(cd "$(dirname "$0")" && pwd)"

# Update packages
sudo apt-get update

# --- Установка Node.js, npm и Yarn ---
echo "Installing Node.js v18 from NodeSource..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install -g yarn

# --- Установка остальных системных зависимостей ---
echo "Installing other system dependencies..."
sudo apt-get install -y \
    git \
    python3 \
    python3-venv \
    python3-dev \
    mariadb-server \
    redis-server \
    curl \
    build-essential

# --- Настройка MariaDB для совместимости с Frappe Bench ---
echo "Configuring MariaDB for Frappe Bench..."
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '${MYSQL_ROOT_PASSWORD:-root}'; FLUSH PRIVILEGES;"

# --- Установка и настройка Frappe Bench ---
# Install bench CLI if not present
if ! command -v bench >/dev/null 2>&1; then
    sudo pip3 install frappe-bench
fi

# Initialize bench directory
if [ ! -d "$BENCH_DIR" ]; then
    sudo -u frappe -H bench init "$BENCH_DIR" --frappe-branch "$FRAPPE_BRANCH"
fi

cd "$BENCH_DIR"

# Create site if it doesn't exist
if ! sudo -u frappe -H bench --site "$SITE_NAME" ls >/dev/null 2>&1; then
    sudo -u frappe -H bench new-site "$SITE_NAME" \
        --admin-password "${ADMIN_PASSWORD:-admin}" \
        --mariadb-root-password "${MYSQL_ROOT_PASSWORD:-root}" \
        --no-mariadb-socket
fi

# Install local app if not installed
if ! sudo -u frappe -H bench list-apps | grep -q "$APP_NAME"; then
    sudo -u frappe -H bench get-app erpnext --branch "$FRAPPE_BRANCH"
    sudo -u frappe -H bench --site "$SITE_NAME" install-app erpnext
    sudo -u frappe -H bench get-app "$APP_NAME" --source-path "$APP_PATH"
    sudo -u frappe -H bench --site "$SITE_NAME" install-app "$APP_NAME"
fi

# Apply migrations and load fixtures
sudo -u frappe -H bench --site "$SITE_NAME" migrate
sudo -u frappe -H bench --site "$SITE_NAME" execute ferum_customs.install.after_install || true

echo "✅ Setup complete. Starting development server..."
sudo -u frappe -H bench start
