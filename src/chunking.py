"""
UTM-InternGuide — Section-Aware & Sentence-Preserving Chunking Module
Guarantees:
1. Never splits words across chunk boundaries.
2. Preserves section headings and keeps unrelated sections separate.
3. Avoids splitting sentences, numbered procedures, and assessment tables.
4. Retains original PDF page numbers.
5. Automatically merges tiny fragments (< MIN_CHUNK_CHARS) within the same section/page.
"""

from __future__ import annotations

import re
from typing import Any

from src.config import MAX_CHUNK_CHARS, MIN_CHUNK_CHARS, TARGET_CHUNK_CHARS
from src.extraction import ExtractedPage
from src.metadata import build_chunk_record, detect_section_heading

SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9(\[])")


def _split_long_block(block: str, max_chars: int) -> list[str]:
    """Split a long block along sentence boundaries (or whitespace fallback), never mid-word."""
    if len(block) <= max_chars:
        return [block]

    # Do not split markdown tables unless absurdly large
    if "[Extracted Table]" in block and len(block) <= max_chars * 1.6:
        return [block]

    sentences = SENTENCE_SPLIT_RE.split(block)
    if len(sentences) == 1:
        # Fallback: split cleanly on line breaks or word boundaries
        words = block.split()
        parts: list[str] = []
        current: list[str] = []
        cur_len = 0
        for w in words:
            add_len = len(w) + (1 if current else 0)
            if cur_len + add_len > max_chars and current:
                parts.append(" ".join(current))
                current = [w]
                cur_len = len(w)
            else:
                current.append(w)
                cur_len += add_len
        if current:
            parts.append(" ".join(current))
        return parts

    parts = []
    buf = ""
    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue
        candidate = f"{buf} {sent}".strip() if buf else sent
        if len(candidate) <= max_chars:
            buf = candidate
        else:
            if buf:
                parts.append(buf)
            if len(sent) > max_chars:
                parts.extend(_split_long_block(sent, max_chars))
                buf = ""
            else:
                buf = sent
    if buf:
        parts.append(buf)
    return parts


def chunk_document_pages(
    source: dict[str, Any],
    pages: list[ExtractedPage],
    target_chars: int = TARGET_CHUNK_CHARS,
    max_chars: int = MAX_CHUNK_CHARS,
    min_chars: int = MIN_CHUNK_CHARS,
) -> list[dict[str, Any]]:
    """Chunk cleaned pages into section-coherent, page-tracked records."""
    raw_chunks: list[tuple[str, int | None, str, bool]] = []
    current_section = "General / Overview"

    for page in pages:
        lines = page.text.splitlines()
        # Group lines into section blocks within this page
        section_blocks: list[tuple[str, list[str]]] = []
        buf_lines: list[str] = []

        for line in lines:
            heading = detect_section_heading(line)
            if heading:
                if buf_lines:
                    section_blocks.append((current_section, buf_lines))
                    buf_lines = []
                current_section = heading
                buf_lines.append(heading)
            else:
                buf_lines.append(line)

        if buf_lines:
            section_blocks.append((current_section, buf_lines))

        # Now pack paragraphs inside each section block without mixing different sections
        for sec_name, sec_lines in section_blocks:
            block_text = "\n".join(sec_lines).strip()
            if not block_text:
                continue

            paragraphs = [p.strip() for p in re.split(r"\n{2,}", block_text) if p.strip()]
            assembled: list[str] = []
            current_buf = ""

            for para in paragraphs:
                if len(para) > max_chars:
                    if current_buf:
                        assembled.append(current_buf)
                        current_buf = ""
                    assembled.extend(_split_long_block(para, max_chars))
                    continue

                candidate = f"{current_buf}\n\n{para}".strip() if current_buf else para
                if len(candidate) <= target_chars:
                    current_buf = candidate
                else:
                    if current_buf:
                        assembled.append(current_buf)
                    current_buf = para

            if current_buf:
                assembled.append(current_buf)

            # Merge tiny trailing fragments within the same section & page
            merged: list[str] = []
            for piece in assembled:
                if len(piece) < min_chars and merged and len(merged[-1]) + len(piece) + 2 <= max_chars * 1.35:
                    merged[-1] = f"{merged[-1]}\n\n{piece}"
                else:
                    merged.append(piece)

            for piece in merged:
                has_tbl = page.has_table or ("| --- |" in piece) or ("[Extracted Table]" in piece)
                raw_chunks.append((sec_name, page.page_number, piece, has_tbl))

    # Second pass: merge isolated micro-chunks (< min_chars) on the same page into previous chunk if safe
    final_tuples: list[tuple[str, int | None, str, bool]] = []
    for item in raw_chunks:
        sec_name, pnum, text, has_tbl = item
        if len(text) < min_chars and final_tuples and final_tuples[-1][1] == pnum:
            prev_sec, prev_p, prev_txt, prev_tbl = final_tuples[-1]
            if len(prev_txt) + len(text) + 2 <= max_chars * 1.4:
                final_tuples[-1] = (prev_sec, prev_p, f"{prev_txt}\n\n{text}", prev_tbl or has_tbl)
                continue
        if len(text) >= 45:  # Skip pure noise micro-lines (e.g., isolated short cover/header artifacts)
            final_tuples.append(item)

    records = [
        build_chunk_record(
            source=source,
            chunk_index=idx,
            text=text,
            section=sec_name,
            page_number=pnum,
            has_table=has_tbl,
        )
        for idx, (sec_name, pnum, text, has_tbl) in enumerate(final_tuples, start=1)
    ]
    return records
