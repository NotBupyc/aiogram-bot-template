project_dir := .
bot_dir := bot

# Lint code
.PHONY: lint
lint:
	@poetry run ruff check $(project_dir)
	@poetry run mypy $(project_dir) --strict

# Reformat code
.PHONY: reformat
reformat:
	@poetry run ruff check $(project_dir) --fix


# Install for dev
.PHONY: install
install-dev:
	@poetry install
	@poetry run pre-commit install

# Install on host
.PHONY: install
install:
	@poetry install --only main


# Start Bot
.PHONY: start
start:
	@poetry run python -m $(bot_dir)

# Make database migration
.PHONY: migration
migration:
	poetry run alembic revision \
	  --autogenerate \
	  --rev-id $(shell python migrations/_get_next_revision_id.py) \
	  --message $(message)

# Migrate
.PHONY: migrate
migrate:
	poetry run alembic upgrade head

.PHONY: stamp
stamp:
	poetry run alembic stamp head
