# version 0.1
FROM python:3.8

ENV APP /app
RUN mkdir $APP
COPY ./src $APP/src

WORKDIR $APP

COPY ./pyproject.toml .
COPY ./requirements.txt .
COPY ./.env .

RUN pip install poetry
RUN pip install python-decouple
RUN pip install -r requirements.txt

RUN POETRY_VIRTUALENVS_CREATE=false poetry install

WORKDIR $APP/src
