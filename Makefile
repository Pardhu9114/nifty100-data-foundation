# ======================================================
# Nifty100 Data Foundation - Makefile
# ======================================================

PYTHON = python

.PHONY: load ratios test report dashboard api clean

# ------------------------------------------------------
# Load all Excel files into SQLite
# ------------------------------------------------------
load:
	$(PYTHON) -m src.etl.run_pipeline

# ------------------------------------------------------
# Generate Financial Ratios
# ------------------------------------------------------
ratios:
	$(PYTHON) -m src.analytics.load_financial_ratios

# ------------------------------------------------------
# Run Test Suite
# ------------------------------------------------------
test:
	$(PYTHON) -m pytest --html=reports/pytest_report.html --self-contained-html

# ------------------------------------------------------
# Generate Reports
# ------------------------------------------------------
report:
	@echo "Report generation is not yet implemented."
	@echo "Please add the report generation script and update this target."

# ------------------------------------------------------
# Launch Streamlit Dashboard
# ------------------------------------------------------
dashboard:
	$(PYTHON) -m streamlit run src/dashboard/app.py

# ------------------------------------------------------
# Launch FastAPI
# ------------------------------------------------------
api:
	$(PYTHON) -m uvicorn src.api.main:app --reload

# ------------------------------------------------------
# Clean cache files
# ------------------------------------------------------
clean:
	$(PYTHON) -c "import pathlib, shutil; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]; [p.unlink() for p in pathlib.Path('.').rglob('*.pyc') if p.exists()]; print('Project cache cleaned.')"