default: help

.PHONY: venv
venv: ## Creates a virtual environment.
	python3.9 -m venv venv

.PHONY: install
install: ## Installs or updates dependencies.
	venv/bin/pip install --upgrade pip
	venv/bin/pip install --upgrade pip-tools
	venv/bin/pip-compile --upgrade
	venv/bin/pip-sync

.PHONY: serve
serve: ## Starts the development server.
	venv/bin/uvicorn main:app --reload

.PHONY: help
help: ## Lists all the available commands.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
