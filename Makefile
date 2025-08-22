.PHONY: install migrate build render-start

install:
	uv sync

migrate:
	uv run python manage.py migrate

collectstatic:
	uv run python manage.py collectstatic --noinput

build:
	./build.sh

render-start:
	uv run gunicorn task_manager.wsgi --bind 0.0.0.0:$${PORT:-8000}