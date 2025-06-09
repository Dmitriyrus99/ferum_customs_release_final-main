# Полная инструкция по установке Ferum Customs

Этот документ описывает последовательные шаги для развёртывания Ferum Customs и ERPNext на сервере Ubuntu.

## 1. Обновление системы
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl wget software-properties-common build-essential
```

## 2. Установка Python 3.10 и pipx
```bash
sudo apt install -y python3.10 python3.10-venv python3.10-dev python3-pip
python3.10 -m pip install --user pipx
python3.10 -m pipx ensurepath
source ~/.bashrc  # или . ~/.profile
```

## 3. Установка Node.js 18 и Yarn
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
sudo npm install -g yarn
```

## 4. Установка Redis
```bash
sudo apt install -y redis-server
sudo systemctl enable redis
sudo systemctl start redis
```

## 5. Установка и настройка MariaDB
```bash
sudo apt install -y mariadb-server
sudo systemctl enable mariadb
sudo systemctl start mariadb
```
При необходимости задайте пароль `root` для пользователя `root`:
```bash
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root'; FLUSH PRIVILEGES;"
```

## 6. Установка wkhtmltopdf
```bash
sudo apt install -y libxrender1 libxext6 libfontconfig1
wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb
sudo apt install -y ./wkhtmltox_0.12.6-1.focal_amd64.deb
```

## 7. Установка Frappe Bench
```bash
pipx install frappe-bench
```

## 8. Клонирование проекта и установка зависимостей
```bash
cd ~
git clone https://github.com/ваш-проект/ferumdub.git
cd ferumdub
./install-dev.sh
./dev_bootstrap.sh
```

## 9. Создание сайта
```bash
cd frappe-bench
sudo bench new-site erp.ferumrus.ru
```
Введите пароль root для MariaDB и задайте пароль администратора.

## 10. Установка приложений
```bash
bench get-app erpnext --branch version-15
bench install-app erpnext
bench get-app ferum_customs /path/to/ferum_customs  # если локально
bench install-app ferum_customs
```

## 11. Запуск сервера разработки
```bash
bench start
```
После запуска интерфейс ERPNext будет доступен по адресу `http://localhost:8000`.

