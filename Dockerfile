FROM python:3.11-slim-buster

WORKDIR /Bot
COPY . .

ENV PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_ROOT_USER_ACTION=ignore

RUN apt-get update && \
    apt-get install -y --no-install-recommends make && \
    pip install poetry && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN make install && poetry update
