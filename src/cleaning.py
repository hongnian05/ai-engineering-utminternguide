"""
UTM-InternGuide — Text Cleaning Module
Cleans extracted PDF and web text while preserving Bahasa Melayu and English content,
section headings, numbered procedures, bullet items, and tabular percentages.
"""

from __future__ import annotations

import re

# Patterns for standalone page numbers or boilerplate running footers
STANDALONE_PAGE_NUM_RE = re.compile(r"^\s*(page\s*)?\d{1,3}(\s*(of|/)\s*\d{1,3})?\s*$", re.IGNORECASE)
BULLET_GLYPHS = {
    "\uf0b7": "-",
    "\uf0a7": "-",
    "\uf071": "-",
    "\uf0d8": "-",
    "\uf0fc": "-",
    "\u2022": "-",
    "\u25aa": "-",
    "\u25cf": "-",
    "\u25cb": "-",
    "\uf0e0": "->",
    "\u2192": "->",
    "\u00a0": " ",
}


def clean_page_text(raw_text: str) -> str:
    """Normalize extracted text without destroying structure or Bahasa Melayu characters."""
    if not raw_text:
        return ""

    text = raw_text.replace("\r\n", "\n").replace("\r", "\n")

    # Replace private-use PDF bullet glyphs with clean ASCII bullets
    for glyph, replacement in BULLET_GLYPHS.items():
        text = text.replace(glyph, replacement)

    # Remove Unicode replacement characters or control chars (except newline/tab)
    text = text.replace("\ufffd", "")
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

    # Repair hyphenated words split across line breaks (e.g., "pre-\nrequisite" -> "prerequisite")
    text = re.sub(r"([A-Za-z]{2,})-\n([a-z]{2,})", r"\1\2", text)

    cleaned_lines: list[str] = []
    for line in text.splitlines():
        stripped = re.sub(r"[ \t]+", " ", line).strip()
        if not stripped:
            if cleaned_lines and cleaned_lines[-1] != "":
                cleaned_lines.append("")
            continue
        # Drop isolated page numbers that add noise
        if STANDALONE_PAGE_NUM_RE.match(stripped):
            continue
        cleaned_lines.append(stripped)

    result = "\n".join(cleaned_lines).strip()
    # Collapse 3+ consecutive newlines into double newline
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result
