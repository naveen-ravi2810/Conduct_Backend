install:
	# make install
	pip install poetry && poetry install
alembic:
	# make alembic
	poetry run alembic upgrade head
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
	chmod +x run.sh
	./run.sh 
debug:
	# make debug
	chmod +x scripts/run.sh
	./scripts/run.sh 

help:
	# make commands help
	@echo ""
	@echo " - install      install all the modules by poetry install"
	@echo " - alembic      DB migration before the application start"
	@echo " - format       apply ruff to format the python file"
	@echo " - lint         runs lint for applied python file"
	@echo " - test		runs pytest for the test files"
	@echo " - debug        runs application in debug mode"
	@echo ""


all : install format lint test start
