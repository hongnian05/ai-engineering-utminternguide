"""
UTM-InternGuide — Faculty-Aware Retriever
Ensures faculty-specific requirements are NEVER mixed across faculties, prioritizes
the user's faculty + University-Wide guidelines, and flags when faculty clarification is needed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from src.config import DEFAULT_TOP_K, FACULTIES, UNIVERSITY_WIDE
from src.vector_store import LocalVectorStore

FACULTY_DETECTION_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\b(fc|faculty of computing|computer science|secr|secj|secv|secb|secd|prisms)\b", re.I), "Faculty of Computing"),
    (re.compile(r"\b(fkt|chemical|energy engineering|bioprocess|petroleum|nuclear)\b", re.I), "Faculty of Chemical and Energy Engineering"),
    (re.compile(r"\b(fke|electrical engineering|ske\*?\s*4926)\b", re.I), "Faculty of Electrical Engineering"),
    (re.compile(r"\b(civil engineering|fka|ska|spaceska)\b", re.I), "Faculty of Civil Engineering"),
    (re.compile(r"\b(mjiit|malaysia-japan|japan internship|ningen-ryoku)\b", re.I), "Malaysia-Japan International Institute of Technology"),
    (re.compile(r"\b(fkm|mechanical engineering|blp-01|blp-02)\b", re.I), "Faculty of Mechanical Engineering"),
]

# Questions whose exact numerical answer varies significantly by faculty
FACULTY_DEPENDENT_PATTERNS = re.compile(
    r"\b(how many credit|credit hour|minimum credit|credits? required|how many weeks|duration|how long|"
    r"cgpa|pngk|eligibility|eligible|qualify|prerequisite|assessment weightage|marks distribution|"
    r"logbook submission|syarat mendaftar|berapa kredit|berapa minggu)\b",
    re.I,
)

# University-wide procedural/system topics that do NOT require faculty clarification
UNIVERSITY_WIDE_TOPICS = re.compile(
    r"\b(its|studentportal|vpn|utmid|international internship|change.*company|bertukar tempat|"
    r"pindah kredit|credit transfer|harassment|unsafe|act 174|2012|2024|senate|senat|conflict|differ)\b",
    re.I,
)


@dataclass
class RetrievalOutput:
    query: str
    detected_faculty: str | None
    allowed_faculties: list[str]
    needs_faculty_clarification: bool
    chunks: list[dict[str, Any]]


def normalize_faculty(faculty_input: str | None) -> str | None:
    if not faculty_input:
        return None
    low = faculty_input.strip().lower()
    if low in FACULTIES:
        return FACULTIES[low]
    for canonical in set(FACULTIES.values()):
        if low == canonical.lower() or low in canonical.lower():
            return canonical
    return None


def detect_faculty_from_query(query: str) -> str | None:
    for pattern, canonical in FACULTY_DETECTION_PATTERNS:
        if pattern.search(query):
            return canonical
    return None


class FacultyAwareRetriever:
    """Retrieves relevant document chunks with strict faculty metadata isolation."""

    def __init__(self, store: LocalVectorStore) -> None:
        self.store = store

    def retrieve(
        self,
        query: str,
        faculty: str | None = None,
        top_k: int = DEFAULT_TOP_K,
        document_type: str | None = None,
        academic_session: str | None = None,
        exclude_historical: bool = False,
    ) -> RetrievalOutput:
        resolved_faculty = normalize_faculty(faculty) or detect_faculty_from_query(query)

        # Check if query asks about a faculty-dependent rule without naming a faculty
        is_faculty_dep = bool(FACULTY_DEPENDENT_PATTERNS.search(query))
        is_uni_wide = bool(UNIVERSITY_WIDE_TOPICS.search(query))
        needs_clarification = (resolved_faculty is None) and is_faculty_dep and not is_uni_wide

        if resolved_faculty and resolved_faculty != UNIVERSITY_WIDE:
            # Strict isolation: ONLY this faculty + University-Wide (+ ITS manual for ITS queries)
            allowed = [resolved_faculty, UNIVERSITY_WIDE]
            if re.search(r"\b(its|studentportal|portal|vpn|utmid|appeal)\b", query, re.I):
                allowed.append("Faculty of Mechanical Engineering")
            chunks = self.store.search(
                query=query,
                top_k=top_k,
                allowed_faculties=allowed,
                document_type=document_type,
                academic_session=academic_session,
                exclude_historical=exclude_historical,
                faculty_boost=resolved_faculty,
            )
        elif resolved_faculty == UNIVERSITY_WIDE or needs_clarification:
            # Restrict to University-Wide documents so we don't mistakenly give one faculty's rules as universal
            allowed = [UNIVERSITY_WIDE]
            if re.search(r"\b(its|studentportal|portal|vpn|utmid)\b", query, re.I):
                allowed.append("Faculty of Mechanical Engineering")
            chunks = self.store.search(
                query=query,
                top_k=top_k,
                allowed_faculties=allowed,
                document_type=document_type,
                academic_session=academic_session,
                exclude_historical=exclude_historical,
            )
        else:
            # General query (e.g., ITS usage, company change, cross-faculty comparison)
            allowed = sorted({r.get("faculty", UNIVERSITY_WIDE) for r in self.store.records})
            chunks = self.store.search(
                query=query,
                top_k=top_k,
                allowed_faculties=None,
                document_type=document_type,
                academic_session=academic_session,
                exclude_historical=exclude_historical,
            )

        return RetrievalOutput(
            query=query,
            detected_faculty=resolved_faculty,
            allowed_faculties=allowed,
            needs_faculty_clarification=needs_clarification,
            chunks=chunks,
        )
