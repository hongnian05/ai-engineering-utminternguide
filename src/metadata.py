"""
UTM-InternGuide — Metadata Extraction & Enrichment Module
Detects section headings, infers language (EN/BM), and builds structured chunk metadata.
"""

from __future__ import annotations

import re
from typing import Any

SECTION_HEADING_PATTERNS = [
    re.compile(r"^(SECTION\s+\d+[:.\-\s].{2,100})$", re.IGNORECASE),
    re.compile(r"^(SEKSYEN\s+\d+[:.\-\s].{2,100})$", re.IGNORECASE),
    re.compile(r"^(BAHAGIAN\s+\d+[:.\-\s].{2,100})$", re.IGNORECASE),
    re.compile(r"^(CHAPTER\s+\d+[:.\-\s].{2,100})$", re.IGNORECASE),
    re.compile(r"^(\d+\.\d+(?:\.\d+)?\s+[A-Za-z][^\n]{2,90})$"),
    re.compile(r"^(\d+\.\s+[A-Z][A-Za-z\s/&\-()]{3,80})$"),
]

BM_MARKERS = {
    "pelajar", "latihan", "industri", "fakulti", "universiti", "syarat",
    "kredit", "hendaklah", "dibenarkan", "laporan", "penilaian", "tempoh",
    "minggu", "penyelia", "garis", "panduan", "mahasiswa", "pendaftaran",
}
EN_MARKERS = {
    "student", "students", "industrial", "training", "faculty", "university",
    "requirement", "requirements", "credit", "credits", "must", "report",
    "evaluation", "duration", "weeks", "supervisor", "guideline", "placement",
}


def detect_section_heading(line: str) -> str | None:
    """Return normalized section heading if line matches an official heading pattern."""
    stripped = line.strip()
    if not stripped or len(stripped) > 110:
        return None
    for pat in SECTION_HEADING_PATTERNS:
        m = pat.match(stripped)
        if m:
            heading = m.group(1).strip()
            # Avoid matching full narrative sentences ending with a period
            if heading.endswith(".") and len(heading) > 70:
                return None
            return heading
    return None


def detect_language(text: str, default_lang: str = "en") -> str:
    """Detect whether chunk text is primarily English, Bahasa Melayu, or bilingual."""
    words = set(re.findall(r"[a-z]+", text.lower()))
    bm_hits = len(words & BM_MARKERS)
    en_hits = len(words & EN_MARKERS)
    if bm_hits >= 2 and en_hits >= 2:
        return "ms/en"
    if bm_hits > en_hits and bm_hits >= 1:
        return "ms"
    if en_hits > bm_hits and en_hits >= 1:
        return "en"
    return default_lang


def build_chunk_record(
    *,
    source: dict[str, Any],
    chunk_index: int,
    text: str,
    section: str,
    page_number: int | None,
    has_table: bool = False,
) -> dict[str, Any]:
    """Build a standardized, provenance-complete chunk record."""
    source_id = source["source_id"]
    chunk_id = f"{source_id}-{chunk_index:04d}"
    version = source.get("document_version") or ""
    is_historical = "historical" in version.lower() or "superseded" in version.lower()

    return {
        "chunk_id": chunk_id,
        "source_id": source_id,
        "document_title": source["document_title"],
        "faculty": source["faculty"],
        "academic_session": source.get("academic_session"),
        "document_version": version or None,
        "publication_or_approval_date": source.get("publication_or_approval_date"),
        "document_type": source.get("document_type"),
        "quality_class": source.get("quality_class"),
        "is_historical": is_historical,
        "section": section,
        "page_number": page_number,
        "language": detect_language(text, default_lang=source.get("language", "en")),
        "has_table": has_table,
        "text": text.strip(),
        "source_url": source.get("source_url"),
        "source_sha256": source.get("verified_sha256") or source.get("sha256"),
    }
