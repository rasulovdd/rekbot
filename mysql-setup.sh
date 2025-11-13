#!/bin/bash

echo "Начало установки и настройки MySQL..."

# 1. Установка MySQL
sudo apt-get update
sudo apt-get install -y mysql-server

# 2. Добавление MySQL в автозагрузку
sudo systemctl enable mysql


# 3. Безопасная настройка базы данных через mysql_secure_installation
echo "Выполнение безопасной настройки MySQL..."
sudo mysql_secure_installation <<EOF

y
y
y
y
EOF

# 4. Создание базы данных и пользователя
echo "Создание базы данных и пользователя..."
sudo mysql <<EOF
CREATE DATABASE IF NOT EXISTS rekbot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'bot_user'@'localhost' IDENTIFIED BY 'bot_password1!';

GRANT ALL PRIVILEGES ON rekbot.* TO 'bot_user'@'localhost';

FLUSH PRIVILEGES;
EOF

# 5. Создание таблиц в базе данных rekbot
echo "Создание таблиц в базе данных rekbot..."
sudo mysql -e "
USE rekbot;

-- Таблица client
CREATE TABLE IF NOT EXISTS client (
  id INT AUTO_INCREMENT PRIMARY KEY,
  date TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  number TEXT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Таблица myusers
CREATE TABLE IF NOT EXISTS myusers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  date TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  user_id BIGINT NOT NULL,
  full_name VARCHAR(255) NULL,
  admin TINYINT(1) NOT NULL DEFAULT 0,
  UNIQUE KEY idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"

# 6. Настройка bind-address (только локальный доступ)
echo "Настройка bind-address для локального доступа..."
sudo sed -i 's/^bind-address.*/bind-address = 127.0.0.1/' /etc/mysql/mysql.conf.d/mysqld.cnf

# Дополнительно: проверяем наличие строки, если её нет — добавляем
if ! grep -q "^bind-address" /etc/mysql/mysql.conf.d/mysqld.cnf; then
    echo "bind-address = 127.0.0.1" | sudo tee -a /etc/mysql/mysql.conf.d/mysqld.cnf
fi

# 7. Установка часового пояса (Москва, UTC+3)
echo "Установка часового пояса UTC+3 (Москва)..."
sudo mysql -e "
SET GLOBAL time_zone = '+03:00';
SET SESSION time_zone = '+03:00';
"

# 8. Перезапуск MySQL для применения изменений
echo "Перезапуск MySQL..."
sudo systemctl restart mysql


# 9. Проверка подключения
echo "Проверка подключения к MySQL..."
if mysql -u bot_user -p'bot_password1!' -e "USE rekbot; SHOW TABLES;" &> /dev/null; then
    echo "✅ MySQL установлен и настроен успешно."
else
    echo "❌ Ошибка подключения к MySQL. Проверьте логин/пароль."
    exit 1
fi

# 10. Вывод итоговой информации
echo ""
echo "=========================================="
echo "ИНФОРМАЦИЯ ДЛЯ ПОДКЛЮЧЕНИЯ"
echo "=========================================="
echo "Пользователь: bot_user"
echo "Пароль: bot_password1!"
echo "База данных: rekbot"
echo "Хост: localhost"
echo "Порт: 3306"
echo "Таблицы:"
echo "  - client"
echo "  - myusers"
echo "=========================================="

echo ""
echo "Скрипт завершён."
