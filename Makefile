PYTHON=python

.PHONY: install run-pipeline start-backend start-frontend test

install:
	pip install -r requirements.txt

run-pipeline:
	PYTHONPATH=. $(PYTHON) backend/pipeline/load_data.py

start-backend:
	PYTHONPATH=. $(PYTHON) -m uvicorn backend.main:app --reload --port 8000

start-frontend:
	streamlit run frontend/app.py

test:
	PYTHONPATH=. pytest -q