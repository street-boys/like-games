FROM python:3.10

WORKDIR /app

COPY . .

RUN apt update && apt install -y netcat

RUN python -m pip install poetry
RUN python -m poetry config virtualenvs.create false && \
    python -m poetry install --no-interaction --no-ansi


CMD echo "[+] Run user" && \
    while !nc -z user_db 5432; do sleep 1; done && \
    uvicorn main:app --reload --host 0.0.0.0 --port 8080
