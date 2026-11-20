"""
UTM-InternGuide — Data Ingestion Module
Loads approved sources from data/source_registry.json and verifies file integrity via SHA-256.
"""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path
from typing import Any

from src.config import BASE_DIR, SOURCE_REGISTRY_PATH

logger = logging.getLogger(__name__)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def load_approved_sources(registry_path: Path = SOURCE_REGISTRY_PATH) -> list[dict[str, Any]]:
    """Load all sources marked include_in_index=True whose raw files exist on disk."""
    if not registry_path.exists():
        raise FileNotFoundError(
            f"Source registry not found at {registry_path}. Run src/build_source_registry.py first."
        )

    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    approved: list[dict[str, Any]] = []
    seen_hashes: set[str] = set()

    for src in registry.get("sources", []):
        if not src.get("include_in_index", False):
            logger.info("Skipping excluded source: %s (%s)", src["source_id"], src.get("access_and_usage_restrictions"))
            continue

        rel_path = src.get("relative_path")
        if not rel_path:
            continue
        full_path = BASE_DIR / rel_path
        if not full_path.is_file():
            logger.warning("Registered source file missing on disk: %s", full_path)
            continue

        current_hash = sha256_file(full_path)
        if current_hash in seen_hashes:
            logger.warning("Duplicate raw file hash detected for %s — skipping duplicate.", src["source_id"])
            continue
        seen_hashes.add(current_hash)

        enriched = dict(src)
        enriched["full_path"] = str(full_path)
        enriched["verified_sha256"] = current_hash
        approved.append(enriched)

    logger.info("Loaded %d approved unique sources from registry.", len(approved))
    return approved
