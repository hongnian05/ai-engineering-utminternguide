"""
UTM-InternGuide — Grounded Answer Generation & Guardrails Module
Supports:
1. Workplace distress / safety escalation guardrail (FR6 / RAI4).
2. Out-of-scope boundary refusal guardrail (FR5 / RAI2).
3. Faculty clarification guardrail when faculty-specific rules are queried without a faculty.
4. Honest abstention when information is absent from verified documents (RAI1).
5. Real OpenAI LLM synthesis when OPENAI_API_KEY is configured in `.env`, OR
   transparent, zero-hallucination local extractive RAG synthesis when no API key is set.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from src.citations import build_citation_dict, format_citations_markdown
from src.config import MIN_SIMILARITY_THRESHOLD, OPENAI_API_KEY, OPENAI_MODEL, PROMPTS_DIR
from src.retriever import RetrievalOutput

logger = logging.getLogger(__name__)

DISTRESS_PATTERNS = re.compile(
    r"\b(harass\w*|sexual\s+harass\w*|bull(y|ied|ying)|discriminat\w*|unsafe|hazard\w*|"
    r"abus(e|ive)|exploit\w*|threaten\w*|assault|suicid\w*|depress\w*|unpaid\s+allowance\s+dispute|"
    r"hostile\s+work|workplace\s+safety\s+violation|grievance)\b",
    re.I,
)

OUT_OF_SCOPE_PATTERNS = re.compile(
    r"\b(bitcoin|crypto|stock\s+market|weather\s+today|recipe|cook\s+nasi|football\s+score|"
    r"medical\s+diagnosis|prescribe\s+medicine|draft\s+a?\s*legal\s+contract|sue\s+my\s+company|"
    r"tax\s+filing|write\s+python\s+game|movie\s+recommend\w*|approve\s+my\s+waiver\s+now)\b",
    re.I,
)


STOPWORDS = {
    "what", "when", "where", "which", "who", "whom", "whose", "why", "how", "does", "did", "can", "could",
    "would", "should", "will", "must", "may", "might", "the", "and", "for", "with", "from", "that", "this",
    "these", "those", "are", "was", "were", "have", "has", "had", "been", "being", "about", "into", "over",
    "after", "before", "under", "between", "during", "through", "utm", "industrial", "training", "internship",
    "student", "students", "intern", "interns", "paid", "exact", "many", "much", "need", "needs", "needed",
    "required", "requirement", "requirements", "apply", "applying", "university", "faculty", "programme",
}


def _has_topic_evidence(query: str, chunks: list[dict[str, Any]]) -> bool:
    """Verify that distinctive non-generic query terms (or their bilingual expansions) appear in retrieved chunks."""
    from src.embeddings import expand_bilingual_query

    q_tokens = [t for t in re.findall(r"[a-zA-Z0-9]{3,}", query.lower()) if t not in STOPWORDS]
    if not q_tokens:
        return True
    combined_ctx = " ".join((c.get("text", "") + " " + c.get("document_title", "")).lower() for c in chunks[:3])
    matched = 0
    for tok in q_tokens:
        expanded_toks = re.findall(r"[a-zA-Z0-9]{2,}", expand_bilingual_query(tok).lower())
        if any(et in combined_ctx for et in expanded_toks):
            matched += 1
    # Require at least 35% of distinctive query terms to be grounded in top-3 chunks
    return (matched / len(q_tokens)) >= 0.35


def _extract_relevant_sentences(query: str, chunks: list[dict[str, Any]], max_sentences: int = 4) -> list[str]:
    """Select the highest-overlap sentences strictly from retrieved chunks (zero invention)."""
    from src.embeddings import expand_bilingual_query

    expanded_q = expand_bilingual_query(query)
    q_terms = {t for t in re.findall(r"[a-zA-Z0-9]{2,}", expanded_q.lower()) if t not in STOPWORDS}
    scored: list[tuple[float, str]] = []
    seen: set[str] = set()

    for rank, ch in enumerate(chunks[:3]):
        text = ch.get("text", "")
        units = re.split(r"(?<=[.!?])\s+|\n+", text)
        for u in units:
            u_clean = " ".join(u.split()).strip()
            if len(u_clean) < 12 or u_clean.startswith("[Extracted Table]") or u_clean.startswith("| ---"):
                continue
            low = u_clean.lower()
            if low in seen:
                continue
            seen.add(low)
            u_terms = set(re.findall(r"[a-zA-Z0-9]{2,}", low))
            overlap = len(q_terms & u_terms)
            has_num = 0.5 if re.search(r"\b\d+(\.\d+)?(%|\s*(weeks?|minggu|credits?|kredit|days?|hari))\b", low) else 0.0
            score = (overlap * 2.0) + (1.0 / (rank + 1)) + has_num
            scored.append((score, u_clean))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [s for _, s in scored[:max_sentences]]


def _call_openai_synthesis(query: str, retrieval: RetrievalOutput, context_blocks: str) -> str | None:
    """Invoke real OpenAI API only when OPENAI_API_KEY is explicitly configured."""
    if not OPENAI_API_KEY:
        return None
    try:
        from openai import OpenAI

        system_prompt_path = PROMPTS_DIR / "system_prompt.md"
        system_prompt = (
            system_prompt_path.read_text(encoding="utf-8")
            if system_prompt_path.exists()
            else "Answer strictly from the provided official UTM context with citations."
        )
        client = OpenAI(api_key=OPENAI_API_KEY)
        user_msg = (
            f"Student Question: {query}\n"
            f"Detected Faculty: {retrieval.detected_faculty or 'Unspecified'}\n"
            f"Needs Faculty Clarification: {retrieval.needs_faculty_clarification}\n\n"
            f"Retrieved Official UTM Context:\n{context_blocks}"
        )
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            temperature=0.1,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg},
            ],
        )
        return resp.choices[0].message.content
    except Exception as exc:
        logger.warning("OpenAI API call failed (%s); falling back to local grounded extraction.", exc)
        return None


def generate_grounded_response(query: str, retrieval: RetrievalOutput) -> dict[str, Any]:
    """Generate a fully grounded, guardrail-checked response with structured citations."""
    # 1. Workplace Distress / Safety Escalation Guardrail (FR6 / RAI4)
    if DISTRESS_PATTERNS.search(query):
        citations = [build_citation_dict(c) for c in retrieval.chunks[:2]]
        answer_text = (
            "**Direct Answer (Official Workplace Safety & Grievance Escalation):**\n"
            "If you are experiencing workplace harassment, discrimination, unsafe working conditions, "
            "or serious workplace grievances during your industrial training, please escalate immediately "
            "through official UTM channels rather than handling it alone:\n\n"
            "- **Faculty Industrial Training Coordinator:** Contact your faculty coordinator immediately "
            "(for Faculty of Computing: `it_coord@comp.utm.my` / `+607-5538888`; for other faculties, contact your respective Faculty Industrial Training Committee).\n"
            "- **UTM Student Counselling Centre:** Seek official university welfare and counselling support.\n"
            "- **Placement Relocation / Termination:** Under UTM Industrial Training guidelines, the faculty reserves the right to review, approve a change of placement, or relocate students when workplace safety or welfare is compromised.\n\n"
            "*Note: UTM-InternGuide cannot provide legal advice or emergency crisis counseling. If you are in immediate physical danger, contact emergency services (999) or UTM Campus Security immediately.*\n\n"
            "**Sources & Citations:**\n" + format_citations_markdown(citations)
        )
        return {
            "mode": "guardrail_distress_escalation",
            "answer": answer_text,
            "citations": citations,
            "abstained": False,
            "needs_faculty_clarification": False,
        }

    # 2. Out-of-Scope Refusal Guardrail (FR5 / RAI2)
    if OUT_OF_SCOPE_PATTERNS.search(query):
        answer_text = (
            "**Direct Answer (Out of Scope):**\n"
            "I am **UTM-InternGuide**, an assistant strictly limited to Universiti Teknologi Malaysia (UTM) "
            "undergraduate Industrial Training (Latihan Industri) policies, procedures, and compliance.\n\n"
            "I cannot assist with out-of-scope legal, medical, financial, or general non-internship requests, "
            "nor can I autonomously approve waivers or placements. Please consult the appropriate professional "
            "or contact your **Faculty Industrial Training Coordinator** for official academic decisions."
        )
        return {
            "mode": "guardrail_out_of_scope",
            "answer": answer_text,
            "citations": [],
            "abstained": True,
            "needs_faculty_clarification": False,
        }

    # 3. Abstention if no sufficiently relevant chunks or topic evidence were retrieved (RAI1)
    top_score = retrieval.chunks[0]["similarity_score"] if retrieval.chunks else 0.0
    if not retrieval.chunks or top_score < MIN_SIMILARITY_THRESHOLD or not _has_topic_evidence(query, retrieval.chunks):
        answer_text = (
            "**Direct Answer:**\n"
            "This information is **not available in the current verified UTM documents** in my knowledge base.\n\n"
            "**Explanation:**\n"
            "- No retrieved document section met the minimum evidence relevance threshold for your question.\n"
            "- To avoid guessing or providing inaccurate academic requirements, please confirm directly with "
            "your **Faculty Industrial Training Coordinator** or the **UTM School of Undergraduate Studies (UGS)**."
        )
        return {
            "mode": "abstention_insufficient_evidence",
            "answer": answer_text,
            "citations": [],
            "abstained": True,
            "needs_faculty_clarification": False,
        }

    citations = [build_citation_dict(c) for c in retrieval.chunks[:3]]

    # Build context blocks for LLM mode
    context_blocks = "\n\n".join(
        f"[{i+1}] Title: {c['document_title']} | Scope: {c['faculty']} | Section: {c['section']} | "
        f"Page: {c.get('page_number')} | Version: {c.get('document_version')}\n{c['text']}"
        for i, c in enumerate(retrieval.chunks[:4])
    )

    # 4. Attempt Real LLM Synthesis if OPENAI_API_KEY is configured
    llm_text = _call_openai_synthesis(query, retrieval, context_blocks)
    if llm_text:
        return {
            "mode": f"llm_rag:{OPENAI_MODEL}",
            "answer": llm_text,
            "citations": citations,
            "abstained": False,
            "needs_faculty_clarification": retrieval.needs_faculty_clarification,
        }

    # 5. Deterministic Local Extractive Grounded RAG Mode (honest offline mode — zero hallucination)
    selected_sentences = _extract_relevant_sentences(query, retrieval.chunks[:3], max_sentences=4)
    has_historical = any(c.get("is_historical") for c in citations)

    parts: list[str] = []
    if retrieval.needs_faculty_clarification:
        parts.append(
            "**Faculty Clarification Needed:**\n"
            "Exact industrial training requirements (such as minimum credit hours, CGPA thresholds, duration, and assessment weightages) "
            "**vary by UTM faculty** (e.g., Faculty of Computing, FKT, FKE, Civil Engineering, MJIIT, FKM). "
            "**Please specify your faculty** for faculty-specific rules.\n\n"
            "**University-Wide Baseline (from verified UTM documents):**"
        )
    else:
        scope_label = retrieval.detected_faculty or "UTM Official Documents"
        parts.append(f"**Direct Answer ({scope_label}):**")

    if selected_sentences:
        parts.append(selected_sentences[0])
        if len(selected_sentences) > 1:
            parts.append("\n**Key Details from Verified Documents:**")
            for sent in selected_sentences[1:]:
                parts.append(f"- {sent}")
    else:
        parts.append(retrieval.chunks[0]["text"][:500])

    if has_historical:
        parts.append(
            "\n> **Version Notice:** One or more retrieved references are from a **historical or superseded edition** "
            "(e.g., 2012 Senate Guideline or 2017/2018 faculty briefing). Please verify current-session details with your Faculty Coordinator."
        )

    parts.append("\n**Sources & Citations:**")
    parts.append(format_citations_markdown(citations))
    parts.append(
        "\n*(Generation Mode: Local Extractive Grounded RAG — set `OPENAI_API_KEY` in `.env` to enable conversational LLM synthesis.)*"
    )

    return {
        "mode": "local_extractive_grounded_rag",
        "answer": "\n".join(parts),
        "citations": citations,
        "abstained": False,
        "needs_faculty_clarification": retrieval.needs_faculty_clarification,
    }
