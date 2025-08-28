install:
	uv sync

dev-install:
	uv sync --group dev

migrate:
	uv run python manage.py migrate

collectstatic:
	uv run python manage.py collectstatic --noinput

run:
	uv run python manage.py runserver

render-start:
	gunicorn task_manager.wsgi

build:
	./build.sh

lint: dev-install
	uv run ruff check

lint-fix:
	uv run ruff check --fix

test: dev-install
	uv run -- python -m pytest -v

coverage: dev-install
	uv run coverage run --source=task_manager --omit='*/migrations/*,*/settings.py,*/venv/*,*/.venv/*' -m pytest
	uv run coverage xml
	uv run coverage report --show-missing --skip-covered


ci-install:
	uv sync --group dev

ci-migrate:
	uv run python manage.py makemigrations --noinput && \
	uv run python manage.py migrate --noinput

ci-test:
	SECRET_KEY="test-secret-key-for-ci" DEBUG=True \
	uv run coverage run --source=task_manager --omit='*/migrations/*,*/settings.py,*/venv/*,*/.venv/*' -m pytest --junitxml=pytest-report.xml
	uv run coverage xml
	uv run coverage report --show-missing --skip-covered