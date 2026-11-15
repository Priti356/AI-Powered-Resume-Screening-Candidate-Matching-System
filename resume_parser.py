"""Extract raw text from PDF and DOCX resume files."""

from pathlib import Path
from zipfile import BadZipFile

import pymupdf
from docx import Document
from docx.opc.exceptions import PackageNotFoundError
from docx.table import Table
from docx.text.paragraph import Paragraph


class ResumeExtractionError(Exception):
    """Raised when a supported resume file cannot be read."""


def extract_resume_text(file_path: str | Path) -> str:
    """Return raw text from a PDF or DOCX file.

    The source file is not modified and the returned text is not normalized.
    Scanned PDFs without a text layer return an empty string; OCR is not
    performed by this module.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Resume file does not exist: {path}")
    if not path.is_file():
        raise ValueError(f"Resume path is not a file: {path}")

    extension = path.suffix.lower()
    if extension == ".pdf":
        return _extract_pdf_text(path)
    if extension == ".docx":
        return _extract_docx_text(path)
    raise ValueError(f"Unsupported resume format: {extension or '(no extension)'}")


def _extract_pdf_text(path: Path) -> str:
    try:
        with pymupdf.open(path) as document:
            if document.needs_pass:
                raise ResumeExtractionError(
                    f"PDF is password-protected and cannot be extracted: {path.name}"
                )
            return "\n".join(page.get_text("text") for page in document)
    except pymupdf.FileDataError as error:
        raise ResumeExtractionError(f"Unable to read PDF resume: {path.name}") from error


def _extract_docx_text(path: Path) -> str:
    try:
        document = Document(path)
    except (BadZipFile, PackageNotFoundError) as error:
        raise ResumeExtractionError(
            f"Unable to read DOCX resume: {path.name}"
        ) from error

    text_blocks: list[str] = []
    for block in document.iter_inner_content():
        if isinstance(block, Paragraph):
            text = block.text.strip()
            if text:
                text_blocks.append(text)
        elif isinstance(block, Table):
            for row in block.rows:
                cells = [
                    " ".join(
                        paragraph.text.strip()
                        for paragraph in cell.paragraphs
                        if paragraph.text.strip()
                    )
                    for cell in row.cells
                ]
                if any(cells):
                    text_blocks.append("\t".join(cells))

    return "\n".join(text_blocks)
