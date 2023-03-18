initialize_git:
	@echo "Initializing git..."
	git init 

activate:
	@echo "Activating virtual environment"
	poetry shell

install: 
	@echo "Installing..."
	poetry install
	poetry run pre-commit install

test:
	pytest

prefect_authenticate:
	@echo "Authenticating with Prefect Cloud..."	
	prefect cloud login

pipeline/request:
	@echo "Requesting data..."
	python src/request.py

pipeline:
	@echo "Running full pipeline..."
	python src/main.py

docs_view:
	@echo View API documentation... 
	PYTHONPATH=src pdoc src --http localhost:8080

docs_save:
	@echo Save documentation to docs... 
	PYTHONPATH=src pdoc src -o docs

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache