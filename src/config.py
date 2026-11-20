"""
UTM-InternGuide — Centralized Configuration
Loads paths, chunking defaults, retrieval parameters, and optional LLM API settings
from environment variables without exposing secrets in source code.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Directory Paths
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
CLEANED_DIR = DATA_DIR / "cleaned"
PROCESSED_DIR = DATA_DIR / "processed"
VECTOR_STORE_DIR = DATA_DIR / "vector_store"
DOCS_DIR = BASE_DIR / "docs"
EVAL_DIR = BASE_DIR / "evaluation"
PROMPTS_DIR = BASE_DIR / "prompts"

# Key Data Artifacts
SOURCE_REGISTRY_PATH = DATA_DIR / "source_registry.json"
COLLECTION_LOG_PATH = DATA_DIR / "collection_log.json"
PROCESSED_CHUNKS_PATH = PROCESSED_DIR / "prepared_text.jsonl"
PIPELINE_MANIFEST_PATH = DATA_DIR / "pipeline_manifest.json"
VECTOR_INDEX_PATH = VECTOR_STORE_DIR / "tfidf_vector_store.pkl"
VECTOR_METADATA_PATH = VECTOR_STORE_DIR / "vector_store_meta.json"

# Chunking Parameters
TARGET_CHUNK_CHARS = 900
MAX_CHUNK_CHARS = 1200
MIN_CHUNK_CHARS = 80
CHUNK_OVERLAP_SENTENCES = 1

# Retrieval Parameters
DEFAULT_TOP_K = 5
MIN_SIMILARITY_THRESHOLD = 0.08

# Canonical Faculty Names
UNIVERSITY_WIDE = "University-Wide"
FACULTIES = {
    "fc": "Faculty of Computing",
    "computing": "Faculty of Computing",
    "fkt": "Faculty of Chemical and Energy Engineering",
    "chemical": "Faculty of Chemical and Energy Engineering",
    "fke": "Faculty of Electrical Engineering",
    "electrical": "Faculty of Electrical Engineering",
    "civil": "Faculty of Civil Engineering",
    "fka": "Faculty of Civil Engineering",
    "ska": "Faculty of Civil Engineering",
    "mjiit": "Malaysia-Japan International Institute of Technology",
    "fkm": "Faculty of Mechanical Engineering",
    "mechanical": "Faculty of Mechanical Engineering",
    "ugs": UNIVERSITY_WIDE,
    "university": UNIVERSITY_WIDE,
    "general": UNIVERSITY_WIDE,
}

# Optional External LLM Configuration (loaded exclusively from environment / .env)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini").strip()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash").strip()
