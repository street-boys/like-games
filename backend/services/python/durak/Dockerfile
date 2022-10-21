FROM python:latest

WORKDIR /app

COPY poetry.lock .
COPY pyproject.toml .

RUN python -m pip install poetry
RUN python -m poetry config virtualenvs.create false && \
    python -m poetry install --no-interaction --no-ansi

COPY . .
