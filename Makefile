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
	venv/bin/uvicorn toolbox:app --reload --host 0.0.0.0

.PHONY: favicon
favicon: ## Builds favicon.ico from favicon.svg.
	@echo "[INFO] Build png with Inkscape:"
	inkscape -w 16 -h 16 -o 16.png favicon.svg
	inkscape -w 32 -h 32 -o 32.png favicon.svg
	inkscape -w 48 -h 48 -o 48.png favicon.svg
	@echo "[INFO] Convert with ImageMagick:"
	convert 16.png 32.png 48.png favicon.ico
	@echo "[INFO] Make sure your ICO contains everything:"
	identify favicon.ico
	@echo "[INFO] Remove temp files:"
	rm 16.png 32.png 48.png


.PHONY: help
help: ## Lists all the available commands.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
