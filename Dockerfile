FROM python:3.11-buster

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry install

COPY . .
