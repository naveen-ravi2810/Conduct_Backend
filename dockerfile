FROM python:3.11-buster

RUN pip install poetry

COPY . .

RUN poetry install

CMD [ "poetry","run","python","main.py" ]

EXPOSE 8000