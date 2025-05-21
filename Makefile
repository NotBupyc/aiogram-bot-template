project_dir := .
bot_dir := bot

.PHONY: docker-run
docker-run:
	@docker-compose up -d

# Start Bot
.PHONY: start
start:
	@poetry run python -m $(bot_dir)

# Install for dev
.PHONY: install-dev
install-dev:
	@poetry install
	@poetry run pre-commit install

# Install on host
.PHONY: install
install:
	@poetry install --only main

# Lint code
.PHONY:	mypy
mypy:
	@poetry run mypy --strict --pretty --explicit-package-bases --install-types bot/ tests/

.PHONY: ruff
ruff:
	@poetry run ruff check bot/ tests/ --fix --respect-gitignore

.PHONY: lint
lint: ruff mypy

.PHONY: tests
tests:
	@poetry run pytest tests/*


# Database
.PHONY: migration
migration:
	@poetry run alembic revision \
	  --autogenerate \
	  --rev-id $(shell poetry run python migrations/_get_next_revision_id.py) \
	  --message $(message)

# Migrate
.PHONY: migrate
migrate:
	@poetry run alembic upgrade head

.PHONY: stamp
stamp:
	@poetry run alembic stamp head
