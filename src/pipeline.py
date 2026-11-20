"""
UTM-InternGuide — End-to-End Data & Vector Indexing Pipeline
Executes:
  1. Source Registry Ingestion (SHA-256 verified)
  2. PDF / Text Extraction (page-by-page with table support)
  3. Text Cleaning (EN & BM preserved)
  4. Section-Aware, Word-Safe Chunking & Metadata Enrichment
  5. Export to data/processed/prepared_text.jsonl + data/pipeline_manifest.json
  6. Automated Data Quality Validation -> docs/data_quality_report.md
  7. Embedding Generation & Persistent Vector Store Build -> data/vector_store/
"""

from __future__ import annotations

import hashlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.chunking import chunk_document_pages
from src.cleaning import clean_page_text
from src.config import (
    CLEANED_DIR,
    DOCS_DIR,
    PIPELINE_MANIFEST_PATH,
    PROCESSED_CHUNKS_PATH,
    PROCESSED_DIR,
)
from src.extraction import ExtractedPage, extract_document
from src.ingestion import load_approved_sources
from src.validation import validate_jsonl_corpus, write_data_quality_report
from src.vector_store import LocalVectorStore

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def run_full_pipeline() -> dict[str, Any]:
    CLEANED_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    sources = load_approved_sources()
    all_chunks: list[dict[str, Any]] = []
    manifest_sources: list[dict[str, Any]] = []

    for src in sources:
        sid = src["source_id"]
        raw_pages = extract_document(src)
        cleaned_pages: list[ExtractedPage] = []

        cleaned_dump_parts: list[str] = []
        for pg in raw_pages:
            cleaned_txt = clean_page_text(pg.text)
            if cleaned_txt:
                cleaned_pages.append(
                    ExtractedPage(
                        source_id=pg.source_id,
                        page_number=pg.page_number,
                        text=cleaned_txt,
                        extraction_method=pg.extraction_method,
                        has_table=pg.has_table,
                    )
                )
                p_label = f"PAGE {pg.page_number}" if pg.page_number is not None else "TEXT"
                cleaned_dump_parts.append(f"=== {p_label} ===\n{cleaned_txt}")

        # Save cleaned text snapshot for inspection
        cleaned_file = CLEANED_DIR / f"{sid}.txt"
        cleaned_file.write_text("\n\n".join(cleaned_dump_parts), encoding="utf-8")

        chunks = chunk_document_pages(src, cleaned_pages)
        all_chunks.extend(chunks)

        manifest_sources.append(
            {
                "source_id": sid,
                "document_title": src["document_title"],
                "faculty": src["faculty"],
                "relative_path": src["relative_path"],
                "source_sha256": src["verified_sha256"],
                "pages_extracted": len(cleaned_pages),
                "chunks_produced": len(chunks),
                "document_version": src.get("document_version"),
            }
        )
        logger.info("Processed %s -> %d pages, %d chunks", sid, len(cleaned_pages), len(chunks))

    # Write prepared JSONL corpus
    with PROCESSED_CHUNKS_PATH.open("w", encoding="utf-8") as f:
        for rec in all_chunks:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    prepared_sha = sha256_file(PROCESSED_CHUNKS_PATH)
    logger.info("Exported %d total chunks to %s", len(all_chunks), PROCESSED_CHUNKS_PATH)

    # Run validation suite & write docs/data_quality_report.md
    val_report = validate_jsonl_corpus(PROCESSED_CHUNKS_PATH)
    write_data_quality_report(val_report, DOCS_DIR / "data_quality_report.md")
    logger.info("Data quality report saved to %s", DOCS_DIR / "data_quality_report.md")

    # Build & persist vector store
    store = LocalVectorStore()
    index_summary = store.build_from_records(all_chunks)
    store.save()

    # Save complete multi-source lineage manifest
    manifest = {
        "pipeline_version": "v2.0-multi-faculty-rag",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "total_sources_processed": len(manifest_sources),
        "total_chunks_exported": len(all_chunks),
        "prepared_output_path": str(PROCESSED_CHUNKS_PATH.relative_to(PROCESSED_CHUNKS_PATH.parents[2])),
        "prepared_output_sha256": prepared_sha,
        "vector_store_summary": index_summary,
        "sources": manifest_sources,
    }
    PIPELINE_MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info("Pipeline manifest saved to %s", PIPELINE_MANIFEST_PATH)

    return {
        "manifest": manifest,
        "validation": val_report,
    }


if __name__ == "__main__":
    run_full_pipeline()
