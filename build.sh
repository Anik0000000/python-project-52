#!/usr/bin/env bash

# Скачиваем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Установка зависимостей
uv sync

# Применяем миграции (КРИТИЧЕСКИ ВАЖНО!)
uv run python manage.py migrate

# Сборка статики
uv run python manage.py collectstatic --noinput