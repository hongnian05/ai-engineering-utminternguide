"""
UTM-InternGuide — Document Extraction Module
Extracts page-by-page text from PDFs using PyMuPDF (with table preservation via pdfplumber
when tables exist and optional OCR only for scanned/image-only pages) and reads TXT sources.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pymupdf

logger = logging.getLogger(__name__)


@dataclass
class ExtractedPage:
    source_id: str
    page_number: int | None
    text: str
    extraction_method: str
    has_table: bool = False


def _format_table_as_markdown(table: list[list[Any]]) -> str:
    """Convert a pdfplumber table matrix into a compact Markdown table."""
    cleaned_rows: list[list[str]] = []
    for row in table:
        if not row:
            continue
        cells = [" ".join((c or "").split()) for c in row]
        if any(cells):
            cleaned_rows.append(cells)
    if len(cleaned_rows) < 2:
        return ""
    col_count = max(len(r) for r in cleaned_rows)
    normalized = [r + [""] * (col_count - len(r)) for r in cleaned_rows]
    header = "| " + " | ".join(normalized[0]) + " |"
    sep = "| " + " | ".join(["---"] * col_count) + " |"
    body = ["| " + " | ".join(r) + " |" for r in normalized[1:]]
    return "\n".join([header, sep] + body)


def _try_ocr_page(page: pymupdf.Page) -> str:
    """Attempt OCR only when a PDF page has almost no selectable text."""
    try:
        import pytesseract
        from PIL import Image

        pix = page.get_pixmap(dpi=200)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        return pytesseract.image_to_string(img, lang="eng")
    except Exception as exc:
        logger.debug("OCR unavailable or failed on page %d: %s", page.number + 1, exc)
        return ""


def extract_pdf_pages(path: Path, source_id: str) -> list[ExtractedPage]:
    """Extract text page-by-page from a PDF, retaining 1-indexed original page numbers."""
    pages: list[ExtractedPage] = []
    doc = pymupdf.open(path)

    # Use pdfplumber selectively for pages containing structured tables
    plumber_tables: dict[int, list[str]] = {}
    try:
        import pdfplumber

        with pdfplumber.open(path) as pdf:
            for idx, ppage in enumerate(pdf.pages, start=1):
                raw_tables = ppage.extract_tables() or []
                md_tables = []
                for tbl in raw_tables:
                    md = _format_table_as_markdown(tbl)
                    if md and len(md) > 30:
                        md_tables.append(md)
                if md_tables:
                    plumber_tables[idx] = md_tables
    except Exception as exc:
        logger.debug("pdfplumber table scan skipped for %s: %s", path.name, exc)

    for page_idx in range(len(doc)):
        page_num = page_idx + 1
        page = doc[page_idx]
        text = page.get_text("text") or ""
        method = "pymupdf-text"

        # Only apply OCR if the page has virtually no selectable text (scanned page)
        if len(text.strip()) < 25:
            ocr_text = _try_ocr_page(page)
            if len(ocr_text.strip()) > len(text.strip()):
                text = ocr_text
                method = "pymupdf+ocr"

        has_table = page_num in plumber_tables
        if has_table:
            # Append structured markdown table representation only if not redundantly huge
            table_block = "\n\n[Extracted Table]\n" + "\n\n".join(plumber_tables[page_num][:2])
            if len(table_block) < 2000:
                text = text.rstrip() + "\n" + table_block
                method += "+pdfplumber-table"

        if text.strip():
            pages.append(
                ExtractedPage(
                    source_id=source_id,
                    page_number=page_num,
                    text=text,
                    extraction_method=method,
                    has_table=has_table,
                )
            )

    doc.close()
    logger.info("Extracted %d non-empty pages from %s", len(pages), path.name)
    return pages


def extract_text_file(path: Path, source_id: str) -> list[ExtractedPage]:
    """Read a plain UTF-8 text source (e.g., webpage extract or local text handbook)."""
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    if not text:
        return []
    return [
        ExtractedPage(
            source_id=source_id,
            page_number=None,
            text=text,
            extraction_method="utf8-text",
            has_table=False,
        )
    ]


def extract_document(source: dict[str, Any]) -> list[ExtractedPage]:
    """Dispatch extraction based on file extension."""
    path = Path(source["full_path"])
    ext = path.suffix.lower()
    if ext == ".pdf":
        return extract_pdf_pages(path, source["source_id"])
    if ext in (".txt", ".md"):
        return extract_text_file(path, source["source_id"])
    raise ValueError(f"Unsupported file extension for extraction: {ext} ({path})")
