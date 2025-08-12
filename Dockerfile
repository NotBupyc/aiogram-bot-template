FROM python:3.11-slim

WORKDIR /bot

# install make
RUN apt-get update && \
    apt-get install -y --no-install-recommends make && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# install poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false

# Copy dependencies
COPY pyproject.toml poetry.lock ./

# install packages
RUN poetry install --no-interaction --no-root

COPY . .
