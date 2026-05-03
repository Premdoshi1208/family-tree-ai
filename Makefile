PYTHON ?= ./venv/bin/python

.PHONY: install run-pipeline dev start start-backend start-frontend test

install:
	$(PYTHON) -m pip install -r requirements.txt

run-pipeline:
	PYTHONPATH=. $(PYTHON) backend/pipeline/load_data.py

dev:
	./scripts/dev.sh

start: dev

start-backend:
	PYTHONPATH=. $(PYTHON) -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

start-frontend:
	$(PYTHON) -m streamlit run frontend/app.py --server.address 127.0.0.1 --server.port 8501

test:
	PYTHONPATH=. $(PYTHON) -m pytest -q
