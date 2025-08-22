install:
	uv sync --dev

migrate:
	python manage.py migrate

collectstatic:
	python manage.py collectstatic --noinput

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi:application --bind 0.0.0.0:$${PORT:-8000}

dev:
	python manage.py runserver 0.0.0.0:8000

lint:
	flake8 .

test:
	python manage.py test