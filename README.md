# UTM-InternGuide — AI-Powered Student Internship Information & Compliance Assistant

> Delivers instant, document-grounded guidance to UTM undergraduate students regarding industrial training eligibility, application procedures, logbook compliance, and regulations, strictly grounded in official university handbooks.

**Author:** Chua Hong Nian (`hongnian05`) | **Course:** SAIA3113 AI Engineering (Semester Project) | **Institution:** Universiti Teknologi Malaysia (UTM)

---

## Problem Statement
Undergraduate students at Universiti Teknologi Malaysia (UTM) frequently face procedural delays, conflicting information, and compliance confusion when preparing for and undertaking mandatory industrial training. Key regulations regarding prerequisite credits, placement approvals, logbook submission schedules, and grading rubrics are dispersed across lengthy PDF guidelines and departmental circulars, overwhelming academic coordinators with repetitive queries during peak registration cycles. UTM-InternGuide provides an AI-engineered, document-grounded 24/7 assistant that provides accurate, policy-verified answers with exact citations, streamlining the advising process and preventing registration failures.

---

## Evidence of the Problem
- **Fragmented Institutional Documentation:** Prerequisite criteria and placement regulations are dispersed across disparate official publications, including the university-wide *Buku Peraturan Akademik Sarjana Muda (Edisi Ke-16)*, the *UTM Senate Industrial Training Guideline (2024)*, and faculty-specific handbooks (such as Computing, Chemical & Energy, Electrical, Civil, Mechanical, and MJIIT), requiring students to cross-examine multi-source documents manually. Across faculties, credit thresholds (80, 90, 99, or 70% earned credits) and durations (12 vs. 20 weeks) differ significantly.
  *(Source: UTM Academic Management, UGS & Faculty Publications, 2015–2025)*
- **Administrative Coordinator Overload:** Academic advisors and internship committee staff spend over 60% of advising time answering routine eligibility and submission inquiries, leading to delayed communication and peak-season bottlenecks.
  *(Source: Al-Shabandar et al., 2021, "Challenges and AI-Driven Interventions in Higher Education Work-Integrated Learning Administration")*

---

## Initial Related Work / Existing Approaches
- **Human Academic & Faculty Industrial Training Coordinators:** Authoritative and highly contextual, but constrained by limited office hours, heavy advising loads during placement deadlines, and potential variance in verbal interpretations across staff.
  *(Source: UTM Faculty Industrial Training Committee Advising Workflow; Key limitation: High latency and non-scalable availability)*
- **Static University FAQ Webpages & Downloadable PDF Portals:** Authoritative and publicly accessible via faculty web portals, the `@studentportal` Industrial Training System (ITS), and PRISMS, but rigid and unable to resolve complex multi-variable conditions (e.g., credit deficiencies combined with overseas placement exemptions).
  *(Source: UTM UGS / ITS / Faculty Portals; Key limitation: Static keyword search and manual navigation burden)*
- **General-Purpose Commercial AI Models (ChatGPT, Claude):** Conversational and accessible 24/7, but entirely ungrounded in UTM-specific institutional rules, resulting in hallucinations of incorrect credit thresholds, non-existent course codes, and unverified academic requirements.
  *(Source: Public OpenAI / Anthropic Foundation Models; Key limitation: High hallucination rate and lack of institutional grounding)*

---

## Engineering Gap / Limitation
Current solutions either rely on labor-intensive human advising that cannot scale during peak placement periods or depend on static document downloads that fail to answer nuanced, multi-document student queries. In contrast, ungrounded commercial LLMs present severe hallucination risks when applied to university compliance. An engineering gap remains for a localized, document-grounded RAG system equipped with faculty-isolated retrieval, dual-layer safety guardrails, and deterministic citation mechanisms tailored to UTM industrial training regulations.

---

## Project Objectives
- **O1:** To design an AI-powered, document-grounded question-and-answering system using Retrieval-Augmented Generation (RAG) that ingests, cleans, chunks, and semantically indexes official UTM Industrial Training regulations and handbooks across multiple faculties.
- **O2:** To develop the RAG pipeline incorporating dual-layer guardrails (faculty clarification, domain-specific input query classification, workplace distress escalation, and citation-backed output verification) to reduce ungrounded or speculative responses.
- **O3:** To evaluate the system objectively across retrieval precision/recall, answer correctness, answer groundedness, citation accuracy, response latency (< 3.0 seconds), and safety refusal rates using a curated benchmark of undergraduate internship scenarios.

---

## Target Users
- **Primary Users:** UTM undergraduate students (primarily Year 3 and Year 4 students in computing and engineering disciplines planning or completing industrial training).
- **Secondary Users:** Faculty Industrial Training Coordinators and Academic Advisors who manage student placements and monitor compliance.

---

## Data Sources
UTM-InternGuide indexes **15 verified official UTM sources** (out of 17 cataloged sources in [`data/source_registry.json`](data/source_registry.json) and [`docs/data_source_inventory.md`](docs/data_source_inventory.md)), covering both university-wide policies and faculty-specific guidelines:

- **University-Wide (UGS / Senate — Class A):**
  - *Garis Panduan Latihan Industri Program Sarjana Muda UTM (2024 Senate Edition, approved 30 April 2024)* — [`ugs.utm.my`](https://ugs.utm.my/industrial-training-li/)
  - *Terms of Reference (ToR) — UTM International Internship Program (2025)* — [`ugs.utm.my`](https://ugs.utm.my/industrial-training-li/)
  - *Garis Panduan Latihan Industri UTM (2012 Senate Edition, approved 15 Feb 2012; hosted under FKT 2022/09 URL and tagged as historical)* — [`GarisPanduanLI.pdf`](https://fkt.utm.my/li/wp-content/uploads/sites/216/2022/09/GarisPanduanLI.pdf)
  - *Buku Peraturan Akademik Program Sarjana Muda Pengajian Sepenuh Masa (Edisi Ke-16, local excerpt)* — [`academicmanagement.utm.my`](https://academicmanagement.utm.my/wp-content/uploads/2021/08/Buku-Peraturan-Akademik-Sarjana-Muda-Edisi-16.pdf)
- **Faculty of Computing (FC — Class B):**
  - *UTM Faculty of Computing Undergraduate Industrial Training Handbook & Guidelines (2023/2024, local excerpt)* — [`comp.utm.my`](https://comp.utm.my/wp-content/uploads/2023/10/Handbook-UG-20232024-1.pdf)
- **Faculty of Chemical and Energy Engineering (FKT — Class B):**
  - *FKT Industrial Training Resources & FAQ Portal* — [`fkt.utm.my/li/resources/`](https://fkt.utm.my/li/resources/)
- **Faculty of Electrical Engineering (FKE — Class B, C, D, E):**
  - *FKE Industrial Training Portal*, *Panduan Pengguna `@studentportal` ITS (Bahasa Melayu, 2024)*, *FKE Briefing Parts I & II (2017/2018, tagged historical)*, and *Application of Potential Company Form* — [`fke.utm.my/li/`](https://fke.utm.my/li/)
- **Faculty of Civil Engineering (Civil / SKA — Class B):**
  - *Industrial Training Guidelines for Undergraduate Programme (7th Edition, 2017, 37 pages)* — [`Guide-Book-Version-7th-2017`](https://civil.utm.my/spaceska/wp-content/blogs.dir/2494/files/2021/07/Guide-Book-Version-7th-2017-reduced-size.pdf)
- **Malaysia-Japan International Institute of Technology (MJIIT — Class B):**
  - *MJIIT Industrial Training Guidebook (2015, 6 pages)* — [`IT-GUIDEBOOK.pdf`](https://mjiit.utm.my/wp-content/uploads/2015/05/IT-GUIDEBOOK.pdf)
- **Faculty of Mechanical Engineering (FKM — Class B & C):**
  - *FKM Industrial Training Portal* and *Portal Usage Guideline for Industrial Training `@studentportal` ITS (English, Dec 2023, 21 pages)* — [`mech.utm.my/industrial-training-fkm/`](https://mech.utm.my/industrial-training-fkm/)

*Note: Third-party restricted sources (such as Scribd) are classified as Class F and excluded from download and indexing.*

---

## RAG Architecture & Data Pipeline Implementation
Building on the V1 conceptual design in [`docs/week2_architecture_v1.png`](docs/week2_architecture_v1.png), the current implementation separates data engineering, retrieval, generation, and evaluation into modular Python components under `src/`:

1. **Data Preparation Pipeline (`src/ingestion.py`, `src/extraction.py`, `src/cleaning.py`, `src/chunking.py`, `src/metadata.py`):**
   - Extracts PDFs page-by-page using PyMuPDF and `pdfplumber` (preserving 1-indexed `page_number` and structured tables), cleans noisy page headers/hyphenations while preserving both **English (`en`)** and **Bahasa Melayu (`ms`)** content, and performs section-aware, word-safe chunking.
   - Produces **406 validated chunks** in `data/processed/prepared_text.jsonl` with full metadata (`chunk_id`, `source_id`, `document_title`, `faculty`, `academic_session`, `document_version`, `is_historical`, `section`, `page_number`, `language`, `source_url`, `source_sha256`).
   - Verified via 13 automated quality checks in `src/validation.py` ([`docs/data_quality_report.md`](docs/data_quality_report.md)).
2. **Bilingual Embeddings & Vector Store (`src/embeddings.py`, `src/vector_store.py`):**
   - Uses hybrid word + character-ngram (`char_wb`) TF-IDF embeddings with an English $\leftrightarrow$ Bahasa Melayu domain synonym expansion dictionary (`406 × 48,667` vectors) stored in `data/vector_store/`.
3. **Faculty-Specific Retrieval (`src/retriever.py`):**
   - Enforces strict faculty metadata filtering (`Faculty of Computing`, `FKT`, `FKE`, `Civil`, `MJIIT`, `FKM`, `University-Wide`) so requirements from one faculty are never mixed into another faculty's answer.
   - Detects when a student asks a faculty-dependent question (e.g., credit hours or duration) without naming a faculty and triggers a **faculty clarification prompt**.
4. **Citation Generation, Safety Guardrails & CLI Prototype (`src/citations.py`, `src/generator.py`, `src/chatbot.py`):**
   - Appends structured citations (document title, faculty/university scope, section, page number, version/session, historical warning if superseded, and source URL).
   - Implements guardrails for workplace harassment/unsafe conditions (immediate official UTM escalation contacts), out-of-scope refusal, and abstention when evidence is missing.
   - Currently operates as a **working CLI prototype** (`python -m src.chatbot`) running in **Local Extractive Grounded RAG Mode** offline, with optional OpenAI API synthesis when `OPENAI_API_KEY` is configured in `.env`.

---

## Evaluation Results
An automated benchmark of **20 test cases** spanning 15 categories (`evaluation/test_questions.jsonl`) was executed against `src/chatbot.py` via `evaluation/run_evaluation.py` (in Local Extractive Grounded RAG Mode). Full per-case logs are recorded in [`evaluation/evaluation_results.json`](evaluation/evaluation_results.json) and [`docs/rag_evaluation_report.md`](docs/rag_evaluation_report.md):

| Evaluation Metric | Measured Result | Target Threshold | Status |
| :--- | :---: | :---: | :---: |
| **Retrieval Precision@3** | **88.9%** | $\ge 60\%$ | ✅ Pass |
| **Retrieval Recall@5** | **100.0%** | $\ge 85\%$ | ✅ Pass |
| **Answer Correctness Rate** | **95.0%** (19/20) | $\ge 85\%$ (NFR2) | ✅ Pass |
| **Answer Groundedness Rate** | **100.0%** | $\ge 95\%$ (RAI1) | ✅ Pass |
| **Citation Correctness Rate** | **100.0%** | $\ge 95\%$ (RAI1) | ✅ Pass |
| **Citation Completeness Rate** | **100.0%** | $100\%$ (FR4) | ✅ Pass |
| **Faculty Isolation Pass Rate** | **100.0%** | $100\%$ | ✅ Pass |
| **Mean / p90 Latency** | **4.26 ms / 5.63 ms** | $< 3,000\text{ ms}$ (NFR1) | ✅ Pass |

---

## Quick Run Instructions (CLI Prototype)
```bash
pip install -r requirements.txt
python -m src.pipeline              # Run ingestion, chunking, validation & vector indexing
python -m src.chatbot -q "How many credit hours do I need?" -f FC
python -m src.chatbot               # Interactive CLI prototype
python evaluation/run_evaluation.py # Re-run the 20-question evaluation benchmark
```

---

## Repository Structure
```text
ai-engineering-utminternguide/
├── README.md                               # Project overview, pipeline summary & weekly log
├── requirements.txt                        # Python dependencies
├── .env.example                            # Optional LLM API key template (.env excluded from git)
├── docs/                                   # Engineering documentation, audits & lab deliverables
│   ├── project_audit.md                    # Comprehensive repository & data audit
│   ├── data_source_inventory.md            # Multi-faculty source classification (A–F) & dates
│   ├── data_quality_report.md              # Automated 13-check data validation report
│   ├── source_conflicts_and_decisions.md   # Cross-faculty & version conflict analysis
│   ├── rag_evaluation_report.md            # 20-question RAG evaluation report
│   ├── week1_observation_sheet.md          # Topic 1 Part A: AI system observation report
│   ├── week1_system_map.png                # Topic 1 Part B: Conceptual AI system map diagram
│   ├── week1_project_scope.md              # Topic 1 Part C: Detailed project scoping document
│   ├── week2_requirements.md               # Topic 2 Part A: FRs, NFRs & RAI requirements
│   ├── week2_evaluation_criteria.md        # Topic 2 Part B: Evaluation criteria table
│   ├── week2_architecture_v1.png           # Topic 2 Part C: V1 system architecture diagram
│   ├── week2_architecture_decisions.md     # Topic 2 Part C: ADRs, trade-offs & RTM
│   ├── week3_data_inventory.md             # Topic 3 Part A: Initial source inventory
│   ├── week3_pipeline_diagram.png          # Topic 3 Part C: Executed V1 pipeline diagram
│   └── week3_pipeline_decisions.md         # Topic 3 Part C: Stage contracts & trade-offs
├── data/                                   # Data engineering pipeline storage & provenance
│   ├── README.md                           # Data directory & transformation documentation
│   ├── source_registry.json                # Structured registry of 17 UTM sources (15 indexed)
│   ├── collection_log.json                 # Automated web/PDF collection log
│   ├── pipeline_manifest.json              # V2 multi-source SHA-256 lineage manifest
│   ├── week3_manifest.json                 # Preserved Week 3 baseline manifest
│   ├── raw/                                # Original sources organized by faculty (PDFs gitignored)
│   ├── cleaned/                            # Page-numbered cleaned text snapshots
│   ├── processed/                          # prepared_text.jsonl (406 chunks) + Week 3 backup
│   ├── pipeline_v1/                        # Preserved Week 3 Part C pipeline artifacts
│   └── vector_store/                       # Persistent local TF-IDF index & metadata
├── notebooks/                              # Executable Colab notebooks
│   └── week3_pipeline.ipynb                # Topic 3 Executable V1 Data Pipeline (Cells 1-9)
├── src/                                    # Modular RAG & data pipeline source code
│   ├── config.py                           # Paths, faculty mappings & env configuration
│   ├── collect_sources.py                  # Official UTM web & PDF source collector
│   ├── build_source_registry.py            # Source registry & SHA-256 generator
│   ├── ingestion.py                        # Approved source loader & duplicate filter
│   ├── extraction.py                       # Page-by-page PDF & table extractor
│   ├── cleaning.py                         # Bilingual text normalizer & hyphen repair
│   ├── metadata.py                         # Section heading & language detector
│   ├── chunking.py                         # Section-aware, word-safe chunker
│   ├── validation.py                       # 13-check data quality validator
│   ├── embeddings.py                       # Bilingual TF-IDF + EN/BM query expansion
│   ├── vector_store.py                     # Metadata-filtered persistent vector store
│   ├── retriever.py                        # Faculty-isolated retriever & clarification logic
│   ├── citations.py                        # Structured citation formatter
│   ├── generator.py                        # Guardrails + OpenAI / extractive RAG generator
│   ├── chatbot.py                          # Chatbot orchestrator & CLI prototype
│   └── pipeline.py                         # End-to-end pipeline runner
├── evaluation/                             # Evaluation benchmarks & results
│   ├── test_questions.jsonl                # 20 ground-truth test cases across 15 categories
│   ├── run_evaluation.py                   # Automated benchmark runner
│   └── evaluation_results.json             # Actual measured evaluation outputs
└── prompts/                                # System prompts and safety guardrail specifications
    ├── system_prompt.md
    └── guardrail_rules.md
```

---

## Weekly Progress
| Week | Focus | Deliverable | Status |
|:---:|:---|:---|:---:|
| **W1** | System map + project scope | README + docs | ✅ |
| **W2** | Requirements, Architecture & Evaluation Criteria | Requirements, Evaluation Benchmarks, V1 Architecture & ADRs | ✅ |
| **W3** | Data Ingestion & Document Chunking | Executable V1 Data Pipeline, Data Inventory, Pipeline Diagram & Lineage Manifest | ✅ |
| **W4** | Vector Embeddings & Retrieval | Multi-source ingestion (`406` chunks), bilingual embeddings, persistent vector store & faculty-isolated retrieval (`src/`) | ✅ |
| **W5** | Prompt Engineering & RAG Generation | System/guardrail prompts (`prompts/`), citation formatter & CLI chatbot prototype (`src/chatbot.py`) | ✅ |
| **W6** | Guardrails & Safety Controls | Distress escalation, out-of-scope refusal, faculty clarification & abstention guardrails (`src/generator.py`) | ✅ |
| **W7** | System Evaluation & Performance Benchmarking | 20-case benchmark (`evaluation/test_questions.jsonl`), automated runner & `docs/rag_evaluation_report.md` | ✅ |

---

## Known Limitations
1. **CLI Prototype Only (No Web Frontend Yet):** The current system runs as a working CLI prototype (`src/chatbot.py`). A complete web-based student frontend still requires implementation.
2. **Live LLM API Integration Unverified:** Because no `OPENAI_API_KEY` is configured in `.env`, the evaluation and CLI currently run in **Local Extractive Grounded RAG Mode**. Live conversational LLM synthesis via OpenAI/Gemini APIs still requires API key configuration and end-to-end verification.
3. **No Absolute Guarantee Against Errors:** While strict grounding, faculty isolation, and guardrails reduce unsupported responses, automated keyword-based evaluation (`95.0%` correctness) cannot guarantee complete accuracy or fluent synthesis in all edge cases, especially when live LLM generation is enabled.
4. **Local Excerpts & Older Faculty Editions:** The Faculty of Computing and Academic Regulations Edisi 16 files from Week 3 are local text excerpts pending full official PDF verification, and several faculty guidebooks (Civil 2017, MJIIT 2015, FKE 2017/2018) predate the April 2024 UTM Senate Guideline.
5. **Copyrighted PDF Redistribution:** Official UTM PDFs under `data/raw/*/*.pdf` are excluded from Git via `.gitignore` to respect institutional copyright; users can reproduce them locally using `python src/collect_sources.py`.
