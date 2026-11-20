"""
UTM-InternGuide — Bilingual Embedding Engine
Uses combined word + character-ngram TF-IDF vectors with a domain-specific EN<->BM
query expansion dictionary so English queries accurately retrieve Bahasa Melayu
official UTM guidelines (and vice versa) with zero external model dependency.
"""

from __future__ import annotations

import re
from typing import Iterable

import numpy as np
from scipy.sparse import hstack, issparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize

# Lightweight domain bilingual synonyms for EN <-> BM UTM industrial training terminology
BILINGUAL_EXPANSIONS: dict[str, list[str]] = {
    "credit": ["kredit", "jam kredit", "kredit dapat"],
    "credits": ["kredit", "jam kredit", "kredit dapat"],
    "kredit": ["credit", "credits"],
    "cgpa": ["pngk", "kedudukan baik", "good standing"],
    "pngk": ["cgpa", "good standing"],
    "standing": ["kedudukan akademik", "kedudukan baik", "kb", "ks"],
    "eligibility": ["syarat mendaftar", "kelayakan", "prasyarat"],
    "eligible": ["syarat mendaftar", "layak"],
    "syarat": ["requirement", "eligibility", "prerequisite"],
    "internship": ["latihan industri", "li", "industrial training"],
    "industrial": ["latihan industri", "li"],
    "training": ["latihan industri", "li"],
    "duration": ["tempoh", "jangkamasa", "jangka masa", "minggu", "weeks"],
    "weeks": ["minggu", "tempoh", "jangkamasa"],
    "minggu": ["weeks", "duration"],
    "insurance": ["insurans", "takaful", "indemnity", "gpa"],
    "insurans": ["insurance", "indemnity"],
    "company": ["syarikat", "organisasi", "tempat li", "host"],
    "change": ["tukar", "bertukar", "pertukaran"],
    "tukar": ["change", "transfer", "relocate"],
    "report": ["laporan", "laporan akhir"],
    "laporan": ["report", "final report"],
    "logbook": ["buku log", "log book", "bi-weekly"],
    "evaluation": ["penilaian", "pemarkahan", "weightage", "marks", "assessment"],
    "assessment": ["penilaian", "evaluation", "weightage", "marks"],
    "supervisor": ["penyelia", "visiting lecturer", "industrial supervisor"],
    "apply": ["mohon", "permohonan", "daftar", "pendaftaran", "application"],
    "application": ["permohonan", "pendaftaran", "apply"],
    "its": ["industrial training system", "studentportal", "sistem latihan industri"],
    "transfer": ["pindah kredit", "pengecualian kredit", "exemption"],
    "exemption": ["pengecualian kredit", "pindah kredit"],
    "defer": ["tangguh", "penangguhan"],
    "fail": ["gagal", "hg", "mengulang"],
    "pass": ["lulus", "hl"],
    "harassment": ["gangguan", "tatatertib", "keselamatan", "grievance", "counselling"],
    "unsafe": ["keselamatan", "osha", "harassment", "grievance"],
    "approved": ["diluluskan", "disahkan", "senat"],
    "senate": ["senat", "diluluskan", "disahkan"],
    "guideline": ["garis panduan", "panduan"],
}


def expand_bilingual_query(query: str) -> str:
    """Append domain-relevant EN<->BM translation terms to improve cross-lingual recall."""
    tokens = re.findall(r"[a-zA-Z0-9]+", query.lower())
    extras: list[str] = []
    for tok in tokens:
        if tok in BILINGUAL_EXPANSIONS:
            extras.extend(BILINGUAL_EXPANSIONS[tok])
    if not extras:
        return query
    return f"{query} " + " ".join(dict.fromkeys(extras))


class BilingualEmbeddingModel:
    """Hybrid word + subword TF-IDF embedding model supporting English and Bahasa Melayu."""

    def __init__(self) -> None:
        self.word_vec = TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True,
            max_features=25000,
            token_pattern=r"(?u)\b\w+\b",
        )
        self.char_vec = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(3, 5),
            sublinear_tf=True,
            max_features=30000,
        )
        self.is_fitted = False

    def fit_transform(self, texts: Iterable[str]):
        text_list = list(texts)
        w = self.word_vec.fit_transform(text_list)
        c = self.char_vec.fit_transform(text_list)
        combined = hstack([w * 1.4, c * 0.8]).tocsr()
        self.is_fitted = True
        return normalize(combined, norm="l2", axis=1)

    def encode_query(self, query: str):
        if not self.is_fitted:
            raise RuntimeError("Embedding model must be fitted before encoding queries.")
        expanded = expand_bilingual_query(query)
        w = self.word_vec.transform([expanded])
        c = self.char_vec.transform([expanded])
        combined = hstack([w * 1.4, c * 0.8]).tocsr()
        return normalize(combined, norm="l2", axis=1)

    @staticmethod
    def cosine_scores(query_vec, doc_matrix) -> np.ndarray:
        scores = doc_matrix @ query_vec.T
        if issparse(scores):
            return scores.toarray().ravel()
        return np.asarray(scores).ravel()
