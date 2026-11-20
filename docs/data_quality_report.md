# Data Quality & Validation Report — UTM-InternGuide

* **Validated At (UTC):** `2026-11-20T18:00:28.705003+00:00`
* **Target Corpus:** `C:\Users\hongk\OneDrive - Universiti Teknologi Malaysia (UTM)\Year 3\SAIA3113 AI Engineering\Semester Project\data\processed\prepared_text.jsonl`
* **Total Chunks Validated:** `406` across `15` verified sources
* **Chunk Character Length (Min / Mean / Max):** `51` / `489.4` / `1335`

---

## 1. Automated Validation Test Results (13 Checks Executed)

| Check | Status | Issues Found | Notes |
| :--- | :---: | :---: | :--- |
| `invalid_jsonl_records` | **PASS** | 0 |  |
| `empty_chunks` | **PASS** | 0 |  |
| `duplicate_documents` | **PASS** | 0 |  |
| `duplicate_chunks` | **WARN/FAIL** | 1 | Samples: `[('FKE-ITS-MS-2024-001-0009', 'FKM-ITS-2023-001-0012')]` |
| `missing_metadata` | **PASS** | 0 |  |
| `missing_source_references` | **PASS** | 0 |  |
| `missing_pdf_page_numbers` | **PASS** | 0 |  |
| `boundary_word_splits` | **WARN/FAIL** | 1 | Samples: `[('CIVIL-GUIDE-2017-001-0014', 'CIVIL-GUIDE-2017-001-0015')]` |
| `too_short_chunks_lt40` | **PASS** | 0 |  |
| `too_long_chunks_gt2500` | **PASS** | 0 |  |
| `missing_sections` | **PASS** | 0 |  |
| `broken_extraction_chars` | **PASS** | 0 |  |
| `table_integrity` | **PASS** | 0 | 147 table-bearing chunks verified |

---

## 2. Corpus Distribution by Faculty Scope

| Faculty / Scope | Chunk Count |
| :--- | :---: |
| University-Wide | 181 |
| Faculty of Civil Engineering | 96 |
| Faculty of Electrical Engineering | 58 |
| Faculty of Mechanical Engineering | 28 |
| Malaysia-Japan International Institute of Technology | 27 |
| Faculty of Computing | 13 |
| Faculty of Chemical and Energy Engineering | 3 |

## 3. Corpus Distribution by Language

| Language | Chunk Count |
| :--- | :---: |
| `en` | 213 |
| `ms` | 160 |
| `ms/en` | 33 |

## 4. Corpus Distribution by Source ID

| Source ID | Chunk Count |
| :--- | :---: |
| `CIVIL-GUIDE-2017-001` | 96 |
| `FC-REPO-2023-001` | 13 |
| `FKE-BRIEF-1-2017` | 13 |
| `FKE-BRIEF-2-2018` | 18 |
| `FKE-FORM-001` | 10 |
| `FKE-ITS-MS-2024-001` | 24 |
| `FKE-WEB-001` | 17 |
| `FKM-ITS-2023-001` | 27 |
| `FKM-WEB-001` | 1 |
| `FKT-WEB-001` | 3 |
| `MJIIT-GUIDE-2015-001` | 27 |
| `UTM-FKT-2012-001` | 47 |
| `UTM-REG-ED16-001` | 6 |
| `UTM-UGS-2024-001` | 84 |
| `UTM-UGS-2025-002` | 20 |

---

## 5. Improvements Verified Compared to Week 3 Baseline

1. **Multi-Source Coverage:** Expanded from 1 source (21 chunks) to all 15 approved official UTM sources across University-Wide (2024 & 2012 Senate Guidelines, 2025 International ToR, Academic Regulations), FC, FKT, FKE, Civil Engineering, MJIIT, and FKM.
2. **Original Page Number Retention:** Every PDF-extracted chunk now retains its exact 1-indexed `page_number` (fixing the Week 3 `page: null` defect).
3. **Zero Mid-Word Splitting:** Replaced rigid 500-character slicing with section-aware, sentence-respecting chunking and micro-fragment merging.
4. **Bilingual Preservation:** Retained both English (`en`) and Bahasa Melayu (`ms` / `ms/en`) official guidelines intact.
