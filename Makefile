install:
	uv sync

collectstatic:
	uv run python manage.py collectstatic --no-input

runserver:
	python manage.py runserver

lint:
	uv run ruff check

migrate:
	uv run python manage.py migrate

test:
	uv run manage.py test

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi