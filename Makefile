SRC_DIR		= src
TEST_DIR	= tests
CHECK_DIRS  = $(SRC_DIR) $(TEST_DIR)


.PHONY: migrate-and-run
migrate-and-run: upgrade-db run ## Run the application and migrate the database 

.PHONY: run
run: ## Run the application
	poetry run python -m pystarter

.PHONY: check
check: format-check lint type-check test ## Launch all the checks (formatting, linting, type checking)

.PHONY: install
install: ## Install the dependencies from the lock file
	poetry install -v

.PHONY: update
update: ## Update python dependencies
	poetry update

.PHONY: format
format: ## Format repository code
	poetry run black $(CHECK_DIRS)
	poetry run isort $(CHECK_DIRS)

.PHONY: format-check
format-check: ## Check the code format with no actual side effects
	poetry run black --check $(CHECK_DIRS)
	poetry run isort --check $(CHECK_DIRS)

.PHONY: lint
lint: ## Launch the linting tool
	poetry run ruff $(SRC_DIR)
	poetry run ruff $(TEST_DIR)

.PHONY: type-check
type-check: ## Launch the type checking tool - currently skipped
	poetry run mypy $(CHECK_DIRS)

.PHONY: test
test: export APP_ENV = test
test: ## Launch the tests
	poetry run python -m pytest -s -vv tests


# DATABASE COMMANDS

.PHONY: generate-migration
generate-migration: ## Generate a new migration
	poetry run alembic revision --autogenerate -m "$(message)"

.PHONY: revert-last-migration
revert-last-migration: ## Revert the last migration
	poetry run alembic downgrade -1

.PHONE: upgrade-db
upgrade-db: ## Upgrade the database to the latest version
	poetry run alembic upgrade head

.PHONY: reset-db
reset-db: ## Reset the database to the latest version
	poetry run alembic downgrade base


.PHONY: help
help: ## Show the available commands
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'