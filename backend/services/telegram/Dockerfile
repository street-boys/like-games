FROM python:3.10

WORKDIR /app

COPY . .

RUN apt update && apt install -y netcat

RUN python -m pip install poetry
RUN python -m poetry config virtualenvs.create false && \
    python -m poetry install --no-interaction --no-ansi


CMD echo "[+] Run telegram" && \
    python main.py
