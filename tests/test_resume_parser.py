from pathlib import Path

import pymupdf
import pytest
from docx import Document

from src.resume_parser import ResumeExtractionError, extract_resume_text


def test_extracts_text_from_pdf(tmp_path: Path) -> None:
    resume_path = tmp_path / "resume.pdf"
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text((72, 72), "Jordan Lee\nPython and data science")
    document.save(resume_path)
    document.close()

    text = extract_resume_text(resume_path)

    assert "Jordan Lee" in text
    assert "Python and data science" in text


def test_extracts_paragraphs_and_tables_from_docx(tmp_path: Path) -> None:
    resume_path = tmp_path / "resume.docx"
    document = Document()
    document.add_paragraph("Jordan Lee")
    table = document.add_table(rows=1, cols=2)
    table.cell(0, 0).text = "Python"
    table.cell(0, 1).text = "Machine learning"
    document.add_paragraph("Experience")
    document.save(resume_path)

    text = extract_resume_text(resume_path)

    assert text.splitlines() == [
        "Jordan Lee",
        "Python\tMachine learning",
        "Experience",
    ]


def test_accepts_uppercase_extension(tmp_path: Path) -> None:
    resume_path = tmp_path / "resume.PDF"
    document = pymupdf.open()
    document.new_page().insert_text((72, 72), "Candidate")
    document.save(resume_path)
    document.close()

    assert "Candidate" in extract_resume_text(resume_path)


def test_rejects_unsupported_format(tmp_path: Path) -> None:
    resume_path = tmp_path / "resume.txt"
    resume_path.write_text("Candidate", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported resume format"):
        extract_resume_text(resume_path)


def test_reports_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="does not exist"):
        extract_resume_text(tmp_path / "missing.pdf")


def test_reports_corrupt_docx(tmp_path: Path) -> None:
    resume_path = tmp_path / "corrupt.docx"
    resume_path.write_text("not a DOCX package", encoding="utf-8")

    with pytest.raises(ResumeExtractionError, match="Unable to read DOCX"):
        extract_resume_text(resume_path)
