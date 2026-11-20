# UTM-InternGuide — AI-Powered Student Internship Information & Compliance Assistant

> A document-grounded, multi-faculty Retrieval-Augmented Generation (RAG) assistant that helps Universiti Teknologi Malaysia (UTM) undergraduate students navigate official industrial training (Latihan Industri) eligibility, procedures, ITS usage, logbooks, insurance, and assessment regulations with verifiable source citations.

**Author:** Chua Hong Nian (`hongnian05`) | **Course:** SAIA3113 AI Engineering (Semester Project) | **Institution:** Universiti Teknologi Malaysia (UTM)

---

## 1. What UTM-InternGuide Does & What Problem It Solves

UTM undergraduate students must cross-reference university-wide Senate guidelines, faculty-specific guidebooks, ITS student manuals, and faculty web portals to determine their industrial training requirements. Requirements **vary significantly across faculties** (for example, credit thresholds range from 80 to 99 credits, and durations vary between 12 and 20 weeks), while older 2012 guidelines are still hosted alongside newer 2024 Senate policies.

**UTM-InternGuide** solves this by:
- Indexing **15 verified official UTM sources** across University-Wide (UGS), Faculty of Computing (FC), Faculty of Chemical & Energy Engineering (FKT), Faculty of Electrical Engineering (FKE), Faculty of Civil Engineering (Civil/SKA), MJIIT, and Faculty of Mechanical Engineering (FKM).
- Enforcing **strict faculty metadata isolation** so Mechanical or Civil Engineering rules are never mixed into a Computing or Chemical Engineering student's answer.
- Providing **structured citations** (document title, faculty/university scope, section, page number, document version/session, and original URL) for every grounded answer.
- Enforcing **safety and scope guardrails** (workplace harassment/unsafe-condition escalation, out-of-scope refusal, faculty clarification prompts, and honest abstention when information is absent).

---

## 2. Target Users
- **Primary Users:** UTM undergraduate students across faculties preparing for or undergoing Industrial Training (Latihan Industri).
- **Secondary Users:** Faculty Industrial Training Coordinators and Academic Advisors.

---

## 3. Data Sources (Verified Multi-Faculty Corpus)

Full details, publication vs. upload dates, SHA-256 hashes, and copyright/redistribution notes are maintained in [`docs/data_source_inventory.md`](docs/data_source_inventory.md) and [`data/source_registry.json`](data/source_registry.json):

| Scope / Faculty | Key Official Sources Indexed |
| :--- | :--- |
| **University-Wide (UGS / Senate)** | *Garis Panduan Latihan Industri UTM (2024 Senate Edition, approved 30 Apr 2024)*; *UTM International Internship Program ToR (2025)*; *2012 Senate Guideline* (tagged historical); *Buku Peraturan Akademik Edisi Ke-16* (local excerpt) |
| **Faculty of Computing (FC)** | *FC Undergraduate Industrial Training Handbook 2023/2024* (local excerpt) |
| **Chemical & Energy Engineering (FKT)** | *FKT Industrial Training Resources & FAQ Portal* |
| **Electrical Engineering (FKE)** | *FKE LI Portal*, *ITS Malay Manual (2024)*, *FKE Briefing Parts I & II (2017/2018, tagged historical)*, *Potential Company Application Form* |
| **Civil Engineering (Civil / SKA)** | *Industrial Training Guidelines 7th Edition (2017, 37 pages)* |
| **MJIIT (UTM KL)** | *MJIIT Industrial Training Guidebook (2015, 6 pages)* |
| **Mechanical Engineering (FKM)** | *FKM Industrial Training Portal*, *ITS `@studentportal` English Manual (Dec 2023, 21 pages)* |

*Third-party restricted sources (e.g., Scribd) are classified as Class F and explicitly **excluded** from download and indexing.*

---

## 4. RAG Architecture

```text
Official UTM PDFs & Web Portals (data/raw/<faculty>/)
  -> Source Registry & SHA-256 Verification (src/ingestion.py)
  -> Page-by-Page PDF & Table Extraction (src/extraction.py — PyMuPDF + pdfplumber)
  -> Bilingual Text Cleaning (src/cleaning.py — EN & BM preserved)
  -> Section-Aware, Word-Safe Chunking & Metadata Tagging (src/chunking.py, src/metadata.py)
  -> 13-Check Automated Data Validation (src/validation.py -> docs/data_quality_report.md)
  -> Bilingual Word + Subword TF-IDF Embeddings (src/embeddings.py)
  -> Metadata-Filtered Persistent Vector Store (src/vector_store.py)
  -> Faculty-Aware Retrieval & Clarification Guardrail (src/retriever.py)
  -> Grounded Answer Generation + Safety Guardrails + Citations (src/generator.py, src/citations.py)
  -> Automated 20-Case Benchmark Evaluation (evaluation/run_evaluation.py)
```

---

## 5. Installation & How to Run

### Prerequisites
- Python 3.10+ (tested on Python 3.12.6 on Windows)

### Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) Configure an OpenAI API key for conversational LLM synthesis
# Copy .env.example to .env and add OPENAI_API_KEY=...
# Without an API key, the chatbot transparently runs in Local Extractive Grounded RAG Mode.
```

### Run the Complete Pipeline & Chatbot
```bash
# 1. Download official publicly accessible UTM sources into data/raw/<faculty>/
python src/collect_sources.py

# 2. Rebuild the structured source registry (SHA-256 + page counts)
python src/build_source_registry.py

# 3. Run full extraction, cleaning, chunking, validation, and vector indexing
python -m src.pipeline

# 4. Ask a question via CLI (with optional faculty filter: FC, FKT, FKE, Civil, MJIIT, FKM)
python -m src.chatbot -q "What is the minimum total credit requirement for Civil Engineering industrial training?" -f Civil

# 5. Launch interactive chatbot session
python -m src.chatbot

# 6. Run the 20-question evaluation benchmark
python evaluation/run_evaluation.py
```

---

## 6. Measured Evaluation Results (Actual Execution)

Evaluated via `evaluation/run_evaluation.py` across 20 test cases spanning all 15 categories (`evaluation/test_questions.jsonl`). Full details in [`docs/rag_evaluation_report.md`](docs/rag_evaluation_report.md):

| Metric | Measured Result | Target | Status |
| :--- | :---: | :---: | :---: |
| **Retrieval Precision@3** | **88.9%** | $\ge 60\%$ | PASS |
| **Retrieval Recall@5** | **100.0%** | $\ge 85\%$ | PASS |
| **Answer Correctness Rate** | **95.0%** (19/20) | $\ge 85\%$ | PASS |
| **Answer Groundedness Rate** | **100.0%** | $\ge 95\%$ | PASS |
| **Citation Correctness Rate** | **100.0%** | $\ge 95\%$ | PASS |
| **Citation Completeness Rate** | **100.0%** | $100\%$ | PASS |
| **Faculty Isolation Pass Rate** | **100.0%** | $100\%$ | PASS |
| **Mean / p90 Latency** | **4.26 ms / 5.63 ms** | $< 3,000\text{ ms}$ | PASS |

---

## 7. Repository Structure

```text
ai-engineering-utminternguide/
├── README.md                                 # Project overview, architecture, setup & measured results
├── requirements.txt                          # Python dependencies
├── .env.example                              # Environment variable template (API keys excluded from git)
├── src/                                      # Modular RAG & data pipeline implementation
│   ├── config.py                             # Paths, faculty mappings, and env-var loading
│   ├── collect_sources.py                    # Official UTM web & PDF downloader
│   ├── build_source_registry.py              # SHA-256 & metadata registry builder
│   ├── ingestion.py                          # Registry loader & duplicate hash filter
│   ├── extraction.py                         # PyMuPDF page-by-page + pdfplumber table extractor
│   ├── cleaning.py                           # Bilingual text normalizer & hyphen repair
│   ├── metadata.py                           # Section heading & language detector
│   ├── chunking.py                           # Section-aware, word-safe chunker with page retention
│   ├── validation.py                         # 13-check data quality validator
│   ├── embeddings.py                         # Bilingual word + char_wb TF-IDF embedder
│   ├── vector_store.py                       # Persistent metadata-filtered vector store
│   ├── retriever.py                          # Faculty-isolated retriever & clarification detector
│   ├── citations.py                          # Structured citation formatter
│   ├── generator.py                          # Guardrails + OpenAI / local extractive RAG generator
│   ├── chatbot.py                            # Main chatbot orchestrator & interactive CLI
│   └── pipeline.py                           # End-to-end ingestion-to-index pipeline runner
├── prompts/                                  # System prompt & safety guardrail specifications
│   ├── system_prompt.md
│   └── guardrail_rules.md
├── evaluation/                               # Automated RAG evaluation suite
│   ├── test_questions.jsonl                  # 20 ground-truth test cases across 15 categories
│   ├── run_evaluation.py                     # Automated benchmark execution script
│   └── evaluation_results.json               # Actual measured per-case evaluation results
├── data/                                     # Raw sources, processed JSONL, manifests & vector store
│   ├── source_registry.json
│   ├── pipeline_manifest.json
│   ├── processed/prepared_text.jsonl         # 406 validated multi-faculty chunks
│   └── vector_store/vector_store_meta.json
├── notebooks/
│   └── week3_pipeline.ipynb                  # Original Week 3 Colab V1 data pipeline notebook
└── docs/                                     # Engineering audits, inventories & weekly deliverables
    ├── project_audit.md                      # Full repository inspection & gap audit
    ├── data_source_inventory.md              # Multi-faculty source classification (A–F) & dates
    ├── data_quality_report.md                # Actual 13-check validation results
    ├── source_conflicts_and_decisions.md     # Cross-faculty & version conflict resolution log
    ├── rag_evaluation_report.md              # Actual 20-case RAG evaluation metrics
    ├── week1_observation_sheet.md
    ├── week1_project_scope.md
    ├── week1_system_map.png
    ├── week2_requirements.md
    ├── week2_evaluation_criteria.md
    ├── week2_architecture_v1.png
    ├── week2_architecture_decisions.md
    ├── week3_data_inventory.md
    ├── week3_pipeline_diagram.png
    └── week3_pipeline_decisions.md
```

---

## 8. Development Progress

| Stage | Focus | Deliverable | Status |
| :---: | :--- | :--- | :---: |
| **W1** | System Map & Project Scope | `README.md`, `week1_project_scope.md`, `week1_system_map.png` | ✅ Complete |
| **W2** | Requirements, Architecture & Evaluation Criteria | `week2_requirements.md`, `week2_architecture_v1.png`, ADRs & RTM | ✅ Complete |
| **W3** | V1 Data Pipeline & Lineage | `week3_pipeline.ipynb`, `week3_pipeline_diagram.png`, `week3_manifest.json` | ✅ Complete |
| **V2 Upgrade** | Multi-Faculty Corpus, Modular RAG, Guardrails & Evaluation | 15 official UTM sources, 406 validated chunks, `src/` RAG modules, `evaluation/` benchmark, audit & conflict docs | ✅ Complete |

---

## 9. Known Limitations

1. **LLM API Key Optional:** No `OPENAI_API_KEY` is bundled in the repository. Out of the box, answers run in **Local Extractive Grounded RAG Mode** (zero hallucination, strict verbatim grounding). Adding an OpenAI API key to `.env` enables fluent conversational synthesis across English and Bahasa Melayu chunks.
2. **Local Excerpts Pending Full Official PDFs:** The Faculty of Computing (`FC-REPO-2023-001`) and Academic Regulations Edisi 16 (`UTM-REG-ED16-001`) files retained from Week 3 are local text excerpts; students/developers should verify against the latest full official PDFs from `comp.utm.my` and `academicmanagement.utm.my`.
3. **Historical Faculty Documents:** Some publicly hosted faculty documents (Civil 2017, MJIIT 2015, FKE 2017/2018 briefings) predate the April 2024 UTM Senate Guideline. They are explicitly labeled when cited, and students are advised to confirm current-session updates with their Faculty Coordinator.
4. **Copyrighted PDF Redistribution:** Downloaded official UTM PDFs under `data/raw/*/*.pdf` are excluded from Git via `.gitignore` to respect UTM copyright; run `python src/collect_sources.py` locally to reproduce them.
