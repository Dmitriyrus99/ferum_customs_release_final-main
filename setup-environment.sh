#!/bin/bash
set -e

APP_NAME="ferum_customs"
SITE_NAME="${SITE_NAME:-dev.localhost}"
FRAPPE_BRANCH="${FRAPPE_BRANCH:-version-15}"
BENCH_DIR="${BENCH_DIR:-/home/frappe/frappe-bench}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

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

sudo -u frappe -H bash "$SCRIPT_DIR/bench_setup.sh" dev

