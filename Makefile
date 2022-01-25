MANAGE = python manage.py
POETRY = poetry run
LOCAL_PORT = http://localhost:8000

all: help
black: ## Format code
	$(POETRY) black ./

check: flake mypy ## Check Python code for problems

check-django: ## Check for Django project problems
	$(MANAGE) check

db: ## Open the database shell
	$(MANAGE) dbshell

flake: ## Lint code
	$(POETRY) flake8 ./

format: isort black ## Format code

help: ## Display the help menu
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

isort: ## Sort imports
	$(POETRY) isort ./

migrate: ## Migrate the database
	$(MANAGE) migrate

migration: ## Make the database migrations
	$(MANAGE) makemigrations

migrations: migration migrate ## Make migrations and migrate

mypy: ## Type-check code
	$(POETRY) mypy ./

run: ## Run the app
	$(MANAGE) runserver

shell: ## Open an app-aware python shell
	$(MANAGE) shell_plus --bpython

superuser: ## Create a user with admin privileges
	$(MANAGE) createsuperuser
