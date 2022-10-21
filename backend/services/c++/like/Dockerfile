FROM gcc:latest

WORKDIR /app/build

CMD echo "[+] Compiling drogon app..." && \
    cmake .. && make && \
    ./like
