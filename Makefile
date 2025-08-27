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

lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix

test:
	uv run pytest -v

coverage:
	uv run coverage run --source=task_manager --omit='*/migrations/*,*/settings.py,*/venv/*,*/.venv/*' -m pytest
	uv run coverage xml
	uv run coverage report --show-missing --skip-covered

test-report:
	chmod +x ./run_tests.sh
	./run_tests.sh
	@if [ -f "coverage.xml" ]; then echo "Coverage report generated successfully"; else echo "ERROR: coverage.xml not generated"; exit 1; fi
	@if [ -f "pytest-report.xml" ]; then echo "Test report generated successfully"; else echo "ERROR: pytest-report.xml not generated"; exit 1; fi

ci-install:
	uv sync --group dev

ci-migrate:
	uv run python manage.py makemigrations --noinput && \
	uv run python manage.py migrate --noinput

ci-test:
	uv run coverage run --source=task_manager --omit='*/migrations/*,*/settings.py,*/venv/*,*/.venv/*' -m pytest
	uv run coverage xml
	uv run coverage report --show-missing --skip-covered