"""
UTM-InternGuide — Structured Citation Formatter
Generates verifiable citations including document title, faculty/university scope,
section, page number (where available), document version/session, historical warning, and source URL.
"""

from __future__ import annotations

from typing import Any


def build_citation_dict(chunk: dict[str, Any]) -> dict[str, Any]:
    return {
        "chunk_id": chunk.get("chunk_id"),
        "source_id": chunk.get("source_id"),
        "document_title": chunk.get("document_title"),
        "faculty_scope": chunk.get("faculty"),
        "section": chunk.get("section") or "General",
        "page_number": chunk.get("page_number"),
        "document_version": chunk.get("document_version"),
        "academic_session": chunk.get("academic_session"),
        "is_historical": bool(chunk.get("is_historical", False)),
        "source_url": chunk.get("source_url"),
        "similarity_score": chunk.get("similarity_score"),
    }


def format_citations_markdown(citations: list[dict[str, Any]]) -> str:
    """Format deduplicated citations cleanly for user-facing responses."""
    if not citations:
        return "No verified document citations available."

    lines: list[str] = []
    seen_keys: set[tuple[Any, ...]] = set()
    idx = 1
    for cit in citations:
        key = (cit["source_id"], cit["section"], cit["page_number"])
        if key in seen_keys:
            continue
        seen_keys.add(key)

        page_str = f"Page {cit['page_number']}" if cit.get("page_number") is not None else "Web/Text Source (No PDF page)"
        ver_str = cit.get("document_version") or cit.get("academic_session") or "Version unspecified"
        hist_note = " **[Historical/Superseded Edition — Verify Current Faculty Rules]**" if cit.get("is_historical") else ""

        lines.append(
            f"{idx}. **{cit['document_title']}**{hist_note}\n"
            f"   - **Scope:** {cit['faculty_scope']}\n"
            f"   - **Section:** {cit['section']} | **Page:** {page_str}\n"
            f"   - **Version / Session:** {ver_str}\n"
            f"   - **Source URL:** {cit['source_url']}"
        )
        idx += 1

    return "\n".join(lines)
