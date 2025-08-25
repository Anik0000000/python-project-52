#!/usr/bin/env bash

# скачиваем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# здесь добавьте все необходимые команды для установки вашего проекта
# команду установки зависимостей, сборки статики, применения миграций и другие
make install && make collectstatic && make migrate

# Установка зависимостей
uv sync

# Применяем миграции (КРИТИЧЕСКИ ВАЖНО!)
uv run python manage.py migrate

# Сборка статики
uv run python manage.py collectstatic --noinput