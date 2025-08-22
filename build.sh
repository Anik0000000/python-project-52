#!/usr/bin/env bash

# Скачиваем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Установка зависимостей
make install
make collectstatic
make migrate