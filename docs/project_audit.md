# Project Audit Report — UTM-InternGuide

* **Project Name:** UTM-InternGuide — AI-Powered Student Internship Information & Compliance Assistant
* **Author:** Chua Hong Nian (`hongnian05`)
* **Repository:** [ai-engineering-utminternguide](https://github.com/hongnian05/ai-engineering-utminternguide)
* **Audit Date:** 2026-11-21
* **Scope:** Complete inspection of repository files, data sources, ingestion pipeline, RAG architecture, code modules, evaluation assets, and documentation.

---

## 1. Executive Summary

UTM-InternGuide currently has strong **Weeks 1–3 conceptual documentation and a prototype V1 data pipeline notebook**, but **no implemented RAG application code, no real multi-faculty official UTM PDF corpus, no vector store, no retrieval/citation engine, and no automated evaluation suite**.

Furthermore, an audit of `data/raw/` and `data/processed/` revealed critical data provenance and quality issues: the two raw files currently stored are compact synthetic summaries (3–6 KB) rather than the full official UTM PDFs, only one of the two inventoried sources was actually processed into `prepared_text.jsonl`, word-splitting occurs across 500-character chunk boundaries, and every existing chunk has `page: null`.

---

## 2. Inventory of Existing Files & Status

| Path | Size | Actual Status |
| :--- | :---: | :--- |
| `README.md` | 8.9 KB | Present; accurately reflects W1–W3 planning, but lists W4–W7 as pending and references only 2–3 sources. |
| `.gitignore` | 356 B | Present; covers `.env`, Python caches, Chroma/FAISS folders, but does not explicitly manage large/restricted third-party PDFs. |
| `docs/week1_observation_sheet.md` | 6.3 KB | Complete Week 1 deliverable. |
| `docs/week1_project_scope.md` | 9.5 KB | Complete Week 1 deliverable. |
| `docs/week1_system_map.png` | 1.09 MB | Complete Week 1 visual diagram. |
| `docs/week2_requirements.md` | 11.2 KB | Complete Week 2 deliverable (FR1–FR7, NFR1–NFR5, RAI1–RAI5). |
| `docs/week2_evaluation_criteria.md` | 5.0 KB | Complete Week 2 deliverable. |
| `docs/week2_architecture_v1.png` | 668 KB | Complete Week 2 conceptual architecture diagram. |
| `docs/week2_architecture_decisions.md` | 8.4 KB | Complete Week 2 ADRs and RTM. |
| `docs/week3_data_inventory.md` | 8.1 KB | Complete Week 3 deliverable, **but claims S02 is verified in `week3_manifest.json` when it is absent.** |
| `docs/week3_pipeline_decisions.md` | 9.2 KB | Complete Week 3 deliverable. |
| `docs/week3_pipeline_diagram.png` | 1.19 MB | Complete Week 3 pipeline diagram (300 DPI). |
| `notebooks/week3_pipeline.ipynb` | 38.9 KB | Executable V1 pipeline notebook, but only processes S01 (`.txt`), uses fixed 500-char fallback splitting, and contains unexecuted cells (`execution_count: null`). |
| `data/raw/utm_fc_industrial_training_handbook_2023_2024.{txt,pdf}` | 6.5 KB / 3.6 KB | **Synthetic/excerpted FC text**, not the full official Faculty of Computing PDF handbook. |
| `data/raw/utm_academic_regulations_edisi_16.{txt,pdf}` | 3.4 KB / 2.2 KB | **Synthetic/excerpted regulations text**, not the full official Edisi 16 PDF. |
| `data/processed/prepared_text.jsonl` | 12.5 KB | Contains 21 chunks from S01 only; `page: null` on all chunks; word-splitting on chunks 0002–0003 and 0007–0008. |
| `data/pipeline_v1/documents/prepared_text.jsonl` | 8.8 KB | Contains 21 chunks from S01 only with reduced schema (`id`, `source`, `text`, `page`). |
| `data/week3_manifest.json` | 710 B | Lists S01 only; omits S02 completely. |
| `data/pipeline_v1/documents/pipeline_manifest.json` | 1.2 KB | Lists S01 only; `inspection.pages: null`. |
| `data/README.md` | 2.3 KB | Outdated placeholder text (`To be populated during Week 3`). |
| `src/` | `.gitkeep` only | **Empty** — no Python modules implemented yet. |
| `evaluation/` | `.gitkeep` only | **Empty** — no test questions or evaluation harness. |
| `prompts/` | `.gitkeep` only | **Empty** — no system or guardrail prompt templates. |
| `requirements.txt` / `.env.example` | Missing | **Not present** — environment reproducibility is undocumented. |

---

## 3. Detailed Audit Findings

### 3.1 What Is Already Implemented & Working
1. **Requirements & Governance Foundation:** Clear functional (FR1–FR7), non-functional (NFR1–NFR5), and Responsible AI (RAI1–RAI5) specifications with measurable thresholds.
2. **Conceptual RAG Architecture:** Appropriate decoupled RAG design with knowledge access, scope/safety guardrails, citation requirements, and evaluation logging.
3. **Lineage & Cryptographic Hashing Pattern:** SHA-256 hashing of raw and processed files in `week3_manifest.json` establishes good provenance habits.
4. **Repository Hygiene:** `.gitignore` properly excludes `.env`, secrets, and local vector index caches.

### 3.2 What Is Incomplete
1. **Zero Application Code (`src/`):** No modular Python implementation exists for ingestion, PDF extraction, cleaning, chunking, metadata processing, embeddings, vector storage, retrieval, answer generation, or citation formatting.
2. **No Multi-Faculty Official Corpus:** Only Faculty of Computing and generic Academic Regulations excerpts exist. Official UTM university-wide guidelines (UGS / 2012 Senate Guideline), Faculty of Chemical & Energy Engineering (FKT), Faculty of Electrical Engineering (FKE), Faculty of Civil Engineering (FKA/SKA), MJIIT, and Faculty of Mechanical Engineering (FKM / ITS Manual) have not been collected or indexed.
3. **No Vector Database & Retrieval Layer:** No embedding generation, persistent vector store, or metadata filtering (by faculty, document type, session, section) exists.
4. **No Evaluation System (`evaluation/`):** No curated ground-truth test set (`test_questions.jsonl`) or automated evaluation runner exists.
5. **No Dependency / Environment Specification:** Missing `requirements.txt` and `.env.example`.

### 3.3 What Is Incorrect or Outdated
1. **Source S02 Missing from Outputs & Manifests:** `docs/week3_data_inventory.md` claims S02 (`utm_academic_regulations_edisi_16`) is verified in `data/week3_manifest.json`, but `week3_manifest.json` and `prepared_text.jsonl` contain **only S01**.
2. **Word Splitting Across Chunks:** Because `paragraph_chunks()` slices paragraphs exceeding 500 characters at rigid character offsets:
   * Chunk `0002` ends mid-sentence and spills `"graduation credits."` (19 chars) into Chunk `0003`.
   * Chunk `0007` splits `"UTM Career Centre"` into `"Ca"` and `"reer Centre."` (12 chars) in Chunk `0008`.
3. **Missing Original Page Numbers:** All 21 chunks in `data/processed/prepared_text.jsonl` have `"page": null` because the pipeline read the `.txt` file instead of extracting page-by-page from PDFs.
4. **Faculty Mixing & Unresolved Terminology Conflicts:**
   * Existing docs refer exclusively to `PRISMS` (FC system), whereas UTM-wide guidelines and FKM manuals use `ITS` (Industrial Training System).
   * Existing docs state a single `80 credit hours` and `20 weeks` rule as if universal, whereas FKT states `90 credits` / 3 years of study, other faculties use `12 weeks`, and the 2012 UTM Senate Guideline explicitly delegates credit thresholds to individual faculties.
5. **Outdated `data/README.md`:** Still contains Week 2 placeholder text.
6. **Stale `.pyc` files in `src/__pycache__/`:** Leftover bytecode files (`features.pyc`, `train_model.pyc`, `utils.pyc`) from an unrelated workflow exist in `__pycache__/` even though `src/` has no `.py` files.

### 3.4 Architecture Suitability Assessment
The **RAG architecture defined in `docs/week2_architecture_v1.png` is well-suited** for UTM-InternGuide (a document-grounded regulatory compliance assistant, not a numerical ML predictor). However, it requires three targeted enhancements to handle UTM's real institutional structure:
1. **Multi-Faculty Metadata Isolation:** Every vector and chunk must carry explicit `faculty` / `scope` metadata (`University-Wide` vs. specific faculty) so retrieval never mixes FKT, FKM, FKE, Civil, MJIIT, and FC rules.
2. **Faculty Clarification Guardrail:** When a student asks a faculty-dependent question (e.g., credit hours, duration, prerequisites) without specifying their faculty, the assistant must ask which faculty they belong to before asserting faculty-specific numbers.
3. **Bilingual (English & Bahasa Melayu) Retrieval Support:** Official UTM guidelines are published in both Bahasa Melayu (e.g., *Garis Panduan Latihan Industri*) and English (e.g., *ITS Student Manual*, *MJIIT IT Guidebook*). The retrieval layer must support both languages without stripping or discarding Bahasa Melayu text.

---

## 4. Recommended Remediation Roadmap

1. **Data Collection & Source Registry:** Inspect and download all publicly accessible official UTM sources (UGS, FKT, FKE, Civil, MJIIT, FKM), verify actual approval/publication dates vs. upload URLs, classify source tiers (A–F), and build `data/source_registry.json` and `docs/data_source_inventory.md`.
2. **PDF Extraction & Improved Chunking Pipeline:** Install a proper PDF library (`pypdf` / `pymupdf`), extract page-by-page text preserving Bahasa Melayu & English, repair broken lines, preserve headings/tables/page numbers, and eliminate word-splitting.
3. **Comprehensive Validation & Conflict Documentation:** Build automated validation (`src/validation.py`) outputting `docs/data_quality_report.md`, and document all cross-faculty/terminology conflicts in `docs/source_conflicts_and_decisions.md`.
4. **Modular RAG Implementation:** Build clean, separated modules under `src/` for ingestion, extraction, cleaning, chunking, metadata, embeddings, vector storage, faculty-aware retrieval, grounded generation (supporting real LLM APIs when configured + transparent deterministic grounded fallback offline), citations, and interactive CLI.
5. **Real End-to-End Evaluation:** Create `evaluation/test_questions.jsonl` covering all 15 required categories, execute real benchmark runs (`evaluation/run_evaluation.py`), save `evaluation/evaluation_results.json`, and publish `docs/rag_evaluation_report.md`.
6. **Documentation Alignment:** Update `README.md`, `requirements.txt`, `.env.example`, and existing `docs/` so every documented claim matches actual tested behavior.
