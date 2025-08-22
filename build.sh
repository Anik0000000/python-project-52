#!/usr/bin/env bash
set -e  # Останавливаем скрипт при ошибках

# Скачиваем и устанавливаем uv
echo "Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Устанавливаем зависимости
echo "Installing dependencies..."
uv sync --production

# Применяем миграции
echo "Applying migrations..."
python manage.py migrate

# Собираем статику
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build completed successfully!"