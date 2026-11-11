# AI-Powered Resume Screening & Candidate Matching System

This repository is being built in stages as a recruiter-assistance tool. It is
intended to help review and compare resumes, not to make hiring decisions.

## Current implementation

The initial stage provides raw text extraction from PDF and DOCX files in
[`src/resume_parser.py`](src/resume_parser.py). It supports local file paths,
rejects unsupported extensions, reports unreadable files, and does not modify
or normalize extracted text. Scanned PDFs without a text layer are not OCR'd.

The NLP, matching, database, dashboard, supervised model, Spark, Kafka, and
Airflow stages have not been implemented yet.

## Windows setup

From the project directory in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest
```

To extract text in Python:

```python
from src.resume_parser import extract_resume_text

text = extract_resume_text(r"C:\path\to\resume.pdf")
```

## Project layout

- `src/`: reusable application modules
- `tests/`: automated tests
- `data/raw/` and `data/processed/`: data staging directories
- `models/`, `database/`, `spark/`, `kafka/`, `airflow/dags/`: planned
  integration areas
- `templates/` and `static/`: planned Flask UI assets
- `notebooks/`: planned analysis notebooks

Dependencies will be added as subsequent project modules are implemented.
