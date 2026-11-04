# V1 Data Pipeline Decisions, Stage Contracts & Traceability — Week 3

**Save as:** `docs/week3_pipeline_decisions.md`  
**Application Name:** UTM-InternGuide (AI-Powered Student Internship Information & Compliance Assistant)  
**Author:** Chua Hong Nian (`hongnian05`)  
**Course:** SAIA3113 AI Engineering — Semester Project  
**Repository:** [ai-engineering-utminternguide](https://github.com/hongnian05/ai-engineering-utminternguide)  

---

## 1. Traceability to Topic 2 Requirements & Architecture

The V1 Data Pipeline implemented in Topic 3 directly materializes the **Offline Ingestion & Indexing Pipeline** established in `docs/week2_architecture_v1.png` and executes the functional capabilities specified in `docs/week2_requirements.md`:

* **FR1 & NFR2 (Prerequisite Accuracy & Correctness $\ge 85\%$):** Requires high-fidelity text extraction of accumulated credit rules (80 credits) and academic standing criteria (Kedudukan Baik) without loss of tabular percentages or prerequisites.
* **FR2 (PRISMS Application Workflow):** Requires sequential extraction of the 5-step registration timeline without rearranging chronological application steps.
* **FR3 (Evaluation Weightages & Logbooks):** Requires preserving the 40% Industry, 30% Visiting Lecturer, and 30% Faculty Committee assessment matrix without splitting numerical values.
* **FR4 & RAI1 (100% Verifiable Source Attribution):** Mandates recording source filename, SHA-256 cryptographic hashes, and chunk record IDs in the prepared dataset to support deterministic page-level citations.
* **NFR4 (Maintainability $< 10\text{ min}$ update):** Demands a modular, scriptable data pipeline where newly published annual handbooks can be re-ingested, validated, and exported without rebuilding unrelated application components.

---

## 2. Part B Preparation Comparison & Observable Evidence

To justify the text segmentation strategy, both **Fixed-Size Chunking** and **Paragraph-Aware Chunking** were executed on the same cleaned source text (`utm_fc_industrial_training_handbook_2023_2024.txt`, 5,612 characters):

| Dimension / Metric | Approach A: Fixed-Size Chunking (`fixed-char-500`) | Approach B: Paragraph-Aware Chunking (`paragraph-aware-char-500`) | Engineering Evidence & Evaluation |
|:---|:---|:---|:---|
| **Resulting Chunk Count** | 12 chunks | 21 chunks | Fixed-size creates fewer, uniform chunks; Paragraph-aware creates granular, topic-specific chunks. |
| **Chunk Size Uniformity** | Exactly 500 characters per chunk (except the final remainder chunk). | Variable size (bounded by 500 characters per segment, respecting natural paragraph breaks). | Paragraph-aware chunks vary in character length but represent coherent administrative policies. |
| **Semantic Integrity (Assessment Matrix)** | Sliced across rows: 40% Industrial Supervisor mark separated from the 30% Visiting Lecturer mark. | Kept intact: Entire Section 4 evaluation breakdown preserved within a self-contained chunk. | Approach B eliminates fragmented criteria that cause retrieval inaccuracies. |
| **Prerequisite Rule Integrity** | Sliced between credit hours condition (80 credits) and CGPA condition (2.00 KB status). | Preserved: Numbered prerequisites (1–4) remain grouped within their parent section context. | Approach B prevents partial retrieval where a student sees only credit hours without learning of CGPA rules. |

### Selected Configuration & Trade-off Justification
* **Selected Configuration:** **Paragraph-Aware Chunking (`paragraph-aware-char-500`)**
* **Benefit:** Guarantees semantic cohesion by aligning chunk boundaries with university handbook headers and numbered procedural steps. When retrieved in Week 4, each context chunk delivers a complete, unambiguous policy rule to the LLM.
* **Accepted Limitation:** Chunks have variable length, requiring downstream vector retrieval similarity thresholds to account for varying token densities. Oversized paragraphs exceeding 500 characters require secondary recursive subdivision.

---

## 3. Core Data Architecture Decisions

### 3.1 ETL vs. ELT Decision
* **Selected Architectural Pattern:** **ETL (Extract, Transform, Load)**
* **Justification:** For a document-grounded RAG application, raw university PDF text contains significant noise (repetitive running headers, erratic whitespace, broken hyphens, unaligned tables). Loading uncleaned text directly into the vector database (ELT) would poison vector embeddings with non-semantic noise and bloat index storage. Applying deterministic transformations (text cleaning, paragraph segmentation, and metadata injection) *before* storage ensures that only clean, verified chunks enter `data/processed/` and `data/pipeline_v1/`.

### 3.2 Batch vs. Streaming Rationale
* **Selected Architectural Pattern:** **Batch Processing**
* **Justification:** Official university academic handbooks and circulars are updated on an annual or semester basis (static institutional publications). There is zero requirement for real-time streaming ingestion. Batch processing guarantees reproducible SHA-256 fingerprinting, zero-cost local execution, and straightforward auditability for academic compliance.

---

## 4. Pipeline Stage Contracts & Failure Handling Matrix

Each pipeline stage enforces an explicit stage contract to guarantee the "Fail-Fast" engineering principle:

| Stage | Expected Contract / Observable Evidence | Failure Mode & Risk | Automated Failure Response |
|:---|:---|:---|:---|
| **1. Ingest** | Explicit source file exists under `data/raw/` and is accessible (`.txt` or `.pdf`). | Missing file path or inaccessible folder. | Raises `FileNotFoundError("Source file not found")` and halts pipeline immediately. |
| **2. Inspect** | Text extraction yields non-empty character string (`len(text) > 0`); detects sections. | Scanned image-only PDF with 0 extractable text characters. | Throws `ValueError("No extractable text found. Scanned PDFs may require OCR.")` to prevent downstream empty processing. |
| **3. Prepare** | Cleans whitespace and splits into coherent chunks according to chosen configuration (`size=500`). | Section exceeds 500 characters without double-line breaks. | Fallback secondary fixed-size splitter subdivides the oversized segment, preventing chunk buffer overflow. |
| **4. Validate** | Output file exists, has non-zero byte size, valid JSONL syntax, and matches record count. | Empty export or malformed JSONL structure. | Assertions `assert prepared_path.stat().st_size > 0` and `assert len(exported) == len(records)` halt pipeline on mismatch. |
| **5. Lineage** | Output SHA-256 fingerprints generated; source-to-output mapping recorded in manifest. | Checksum mismatch or missing output record. | Halts execution during Cell 6B / Cell 9 repeatability verification on fingerprint discrepancy. |

---

## 5. Requirements Traceability Matrix (Data Engineering Stage)

| Objective | Requirement ID | Pipeline Stage & Component | Verification Evidence / Artefact |
|:---:|:---|:---|:---|
| **O1** | **FR1 / FR3** (Prerequisites & Assessment Rules) | Ingest (`utm_fc_handbook`) $\rightarrow$ Paragraph Chunking | `data/processed/prepared_text.jsonl` (21 verified chunks preserving policy clauses) |
| **O1** | **FR4 / RAI1** (Source Citation Attribution) | Metadata Enrichment $\rightarrow$ Lineage Registration | `data/week3_manifest.json` recording source name, SHA-256 hashes, and chunk record IDs |
| **O2** | **NFR2** (Answer Correctness $\ge 85\%$) | Text Normalization & Layout Preservation | Inspection evidence showing intact 40%/30%/30% assessment matrix and 80-credit thresholds |
| **O3** | **NFR4** (Maintainability $< 10\text{ min}$) | Reusable `execute_pipeline()` engine | Automated Cell 9 Repeatability Smoke Test passing with identical cryptographic fingerprints |

---

## 6. Topic 3 Reflection

> **Reflection Question:** *Which pipeline stage contract is most critical to downstream AI system performance, and what trade-off did you accept during data preparation?*

**Reflection:**  
The most critical pipeline stage contract is **Stage 4 (Prepare / Text Segmentation)** linked to **Stage 5 (Validation)**. In a Retrieval-Augmented Generation system, the retrieval engine cannot retrieve what the data preparation pipeline destroyed. If the text splitter naively slices through a prerequisite rule (e.g., separating the 80 credit hour threshold from the 2.00 CGPA requirement across two different chunks), the downstream LLM will receive fragmented context and inevitably produce an incorrect or ungrounded answer, directly violating NFR2.

During data preparation, the most important trade-off accepted was choosing **Paragraph-Aware Chunking over Fixed-Size Chunking**. Fixed-size chunking produced fewer, predictably uniform chunks (12 chunks of 500 characters) that were simple to index. However, it regularly severed numbered lists and policy tables. We accepted the trade-off of **higher chunk count variance** (21 chunks of varying lengths) in exchange for **complete semantic cohesion and bullet-point preservation**. This deliberate trade-off guarantees that every retrieved chunk represents an authoritative, stand-alone institutional policy clause.
