"""
UTM-InternGuide — Persistent Vector Store with Metadata Filtering
Stores embeddings alongside full chunk metadata, supports deduplication, version tracking,
clean re-ingestion, and metadata-filtered cosine similarity search.
"""

from __future__ import annotations

import json
import logging
import pickle
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

from src.config import VECTOR_INDEX_PATH, VECTOR_METADATA_PATH, VECTOR_STORE_DIR
from src.embeddings import BilingualEmbeddingModel

logger = logging.getLogger(__name__)


class LocalVectorStore:
    """Persistent vector store supporting metadata filters and version-aware re-ingestion."""

    def __init__(self) -> None:
        self.model = BilingualEmbeddingModel()
        self.matrix = None
        self.records: list[dict[str, Any]] = []
        self.built_at_utc: str | None = None

    def build_from_records(self, records: list[dict[str, Any]]) -> dict[str, Any]:
        """Deduplicate records by chunk_id/text, fit embeddings, and build index."""
        unique_records: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        seen_texts: set[str] = set()

        for rec in records:
            cid = rec["chunk_id"]
            txt = rec["text"].strip()
            norm_key = f"{rec.get('source_id')}::{txt.lower()}"
            if cid in seen_ids or norm_key in seen_texts or not txt:
                continue
            seen_ids.add(cid)
            seen_texts.add(norm_key)
            unique_records.append(rec)

        # Embed section + document title + text for richer semantic matching
        embed_texts = [
            f"{r.get('document_title', '')} | {r.get('faculty', '')} | {r.get('section', '')}\n{r['text']}"
            for r in unique_records
        ]
        self.records = unique_records
        self.matrix = self.model.fit_transform(embed_texts)
        self.built_at_utc = datetime.now(timezone.utc).isoformat()

        logger.info(
            "Built vector index with %d unique chunks (shape=%s).",
            len(self.records),
            self.matrix.shape,
        )
        return {
            "total_vectors": len(self.records),
            "vector_dim": int(self.matrix.shape[1]),
            "built_at_utc": self.built_at_utc,
            "sources_indexed": sorted({r["source_id"] for r in self.records}),
        }

    def save(
        self,
        index_path: Path = VECTOR_INDEX_PATH,
        meta_path: Path = VECTOR_METADATA_PATH,
    ) -> None:
        VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
        payload = {
            "model": self.model,
            "matrix": self.matrix,
            "records": self.records,
            "built_at_utc": self.built_at_utc,
        }
        with index_path.open("wb") as f:
            pickle.dump(payload, f)

        summary = {
            "built_at_utc": self.built_at_utc,
            "total_vectors": len(self.records),
            "vector_dim": int(self.matrix.shape[1]) if self.matrix is not None else 0,
            "faculties": sorted({r.get("faculty", "Unknown") for r in self.records}),
            "sources": sorted({r.get("source_id", "Unknown") for r in self.records}),
        }
        meta_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
        logger.info("Saved vector store to %s", index_path)

    @classmethod
    def load(cls, index_path: Path = VECTOR_INDEX_PATH) -> "LocalVectorStore":
        if not index_path.exists():
            raise FileNotFoundError(f"Vector store not found at {index_path}. Run src/pipeline.py first.")
        with index_path.open("rb") as f:
            payload = pickle.load(f)
        store = cls()
        store.model = payload["model"]
        store.matrix = payload["matrix"]
        store.records = payload["records"]
        store.built_at_utc = payload.get("built_at_utc")
        return store

    def search(
        self,
        query: str,
        top_k: int = 5,
        allowed_faculties: list[str] | None = None,
        document_type: str | None = None,
        academic_session: str | None = None,
        section_contains: str | None = None,
        language: str | None = None,
        exclude_historical: bool = False,
        faculty_boost: str | None = None,
    ) -> list[dict[str, Any]]:
        """Perform metadata-filtered cosine similarity search with authority/recency weighting."""
        if self.matrix is None or not self.records:
            return []

        q_vec = self.model.encode_query(query)
        raw_scores = self.model.cosine_scores(q_vec, self.matrix)

        candidates: list[tuple[float, float, dict[str, Any]]] = []
        for idx, rec in enumerate(self.records):
            if allowed_faculties is not None and rec.get("faculty") not in allowed_faculties:
                continue
            if document_type and document_type.lower() not in (rec.get("document_type") or "").lower():
                continue
            if academic_session and academic_session.lower() not in (rec.get("academic_session") or "").lower():
                continue
            if section_contains and section_contains.lower() not in (rec.get("section") or "").lower():
                continue
            if language and language.lower() not in (rec.get("language") or "").lower():
                continue
            if exclude_historical and rec.get("is_historical"):
                continue

            base_score = float(raw_scores[idx])
            if base_score <= 0.0:
                continue

            # Authority/recency weighting: faculty-specific rules take priority over university-wide baseline
            adjusted = base_score
            if faculty_boost and rec.get("faculty") == faculty_boost:
                adjusted *= 2.25
            if rec.get("source_id") == "UTM-UGS-2024-001":
                adjusted *= 1.12
            if rec.get("is_historical"):
                adjusted *= 0.85

            candidates.append((adjusted, base_score, rec))

        candidates.sort(key=lambda x: x[0], reverse=True)
        results: list[dict[str, Any]] = []
        for adj, raw, rec in candidates[:top_k]:
            item = dict(rec)
            item["similarity_score"] = round(raw, 4)
            item["ranked_score"] = round(adj, 4)
            results.append(item)
        return results
