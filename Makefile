install:
	# make install
	pip install poetry && poetry update
format:
	# make format
	ruff format
lint:
	# make lint
	pylint *.py
test:
	# make test
	python -m pytest --cov=tests