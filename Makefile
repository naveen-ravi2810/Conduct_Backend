install:
	# make install
	pip install poetry && poetry update
alembic:
	# make alembic
	alembic upgrade head
format:
	# make format
	ruff format
lint:
	# make lint
	find . -name "*.py" -exec pylint {} +
test:
	# make test
	python -m pytest -qvs tests/
start:
	# make start
	uvicorn main:app --host=0.0.0.0 --port=8000

all : install format lint test start
