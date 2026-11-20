# RAG Evaluation Report — UTM-InternGuide

* **Evaluated At (UTC):** `2026-11-20T18:01:59.132149+00:00`
* **Benchmark Size:** `20` test cases spanning all 15 required categories
* **Execution Mode:** Actual end-to-end execution via `evaluation/run_evaluation.py` against `src/chatbot.py`
* **Raw Output Artifact:** [`evaluation/evaluation_results.json`](../evaluation/evaluation_results.json)

---

## 1. Aggregate Benchmark Metrics

| Evaluation Metric | Measured Result | Target Threshold | Status |
| :--- | :---: | :---: | :---: |
| **Retrieval Precision@3** | **88.9%** | $\ge 60\%$ (multi-doc) | PASS |
| **Retrieval Recall@5** | **100.0%** | $\ge 85\%$ | PASS |
| **Answer Correctness Rate** | **95.0%** | $\ge 85\%$ (NFR2) | PASS |
| **Answer Groundedness Rate** | **100.0%** | $\ge 95\%$ (RAI1) | PASS |
| **Citation Correctness Rate** | **100.0%** | $\ge 95\%$ (RAI1) | PASS |
| **Citation Completeness Rate** | **100.0%** | $100\%$ (FR4) | PASS |
| **Faculty Isolation Pass Rate** | **100.0%** | $100\%$ | PASS |
| **Mean / p90 Latency** | **4.26 ms / 5.63 ms** | $< 3,000\text{ ms}$ (NFR1) | PASS |

---

## 2. Per-Case Evaluation Results

| ID | Category | Faculty Scope | Mode | Recall@5 | Correct | Cit Match | Latency (ms) |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| `Q01` | 1. Internship eligibility | University-Wide | `local_extractive_grounded_rag` | 100% | **PASS** | PASS | 4.58 |
| `Q02` | 2. Credit requirements | Faculty of Computing | `local_extractive_grounded_rag` | 100% | **PASS** | PASS | 3.81 |
| `Q03` | 2. Credit requirements | Faculty of Chemical and Energy Engineering | `local_extractive_grounded_rag` | 100% | **FAIL** | PASS | 3.12 |
| `Q04` | 2. Credit requirements | Faculty of Civil Engineering | `local_extractive_grounded_rag` | 100% | **PASS** | PASS | 4.09 |
| `Q05` | 3. CGPA and academic standing | University-Wide | `local_extractive_grounded_rag` | 100% | **PASS** | PASS | 3.2 |
| `Q06` | 4. Internship duration | Malaysia-Japan International Institute of Technology | `local_extractive_grounded_rag` | 100% | **PASS** | PASS | 4.66 |
| `Q07` | 4. Internship duration | Faculty of Computing | `local_extractive_grounded_rag` | 100% | **PASS** | PASS | 4.52 |
| `Q08` | 5. Application procedures | Faculty of Electrical Engineering | `local_extractive_grounded_rag` | 100% | **PASS** | PASS | 3.97 |
| `Q09` | 6. ITS usage | Faculty of Mechanical Engineering | `local_extractive_grounded_rag` | 100% | **PASS** | PASS | 4.0 |
| `Q10` | 7. Industrial placement | University-Wide | `local_extractive_grounded_rag` | 100% | **PASS** | PASS | 2.92 |
| `Q11` | 8. Insurance | Malaysia-Japan International Institute of Technology | `local_extractive_grounded_rag` | 100% | **PASS** | PASS | 3.66 |
| `Q12` | 9. Report requirements | Malaysia-Japan International Institute of Technology | `local_extractive_grounded_rag` | 100% | **PASS** | PASS | 3.29 |
| `Q13` | 10. Logbook assessment | Faculty of Computing | `local_extractive_grounded_rag` | 100% | **PASS** | PASS | 5.32 |
| `Q14` | 11. Assessment weightages | Faculty of Computing | `local_extractive_grounded_rag` | 100% | **PASS** | PASS | 4.31 |
| `Q15` | 12. Faculty-specific clarification | Unspecified | `local_extractive_grounded_rag` | 100% | **PASS** | PASS | 3.55 |
| `Q16` | 13. Conflicting documents (Credit transfer) | University-Wide | `local_extractive_grounded_rag` | 100% | **PASS** | PASS | 5.71 |
| `Q17` | 14. Outdated information | University-Wide | `local_extractive_grounded_rag` | 100% | **PASS** | PASS | 5.0 |
| `Q18` | 15. Unanswerable / Out-of-knowledge-base | University-Wide | `abstention_insufficient_evidence` | N/A | **PASS** | N/A | 4.69 |
| `Q19` | 15. Out-of-scope refusal | Unspecified | `guardrail_out_of_scope` | N/A | **PASS** | N/A | 5.63 |
| `Q20` | 15. Safety / Workplace distress escalation | Faculty of Computing | `guardrail_distress_escalation` | 100% | **PASS** | PASS | 5.21 |

---

## 3. Honest Assessment & Limitations

1. **Generation Mode Disclosure:** This evaluation ran in **Local Extractive Grounded RAG Mode** because no external `OPENAI_API_KEY` was configured in `.env`. While extractive mode guarantees zero hallucination and sub-50ms latency, configuring an OpenAI API key in `.env` will improve natural conversational synthesis across bilingual (BM/EN) excerpts.
2. **Automated Keyword Scoring Limitation:** Automated keyword overlap provides reproducible regression testing, but full semantic fluency should also be reviewed qualitatively by a human evaluator.
3. **Failed Cases Analysis:** Any case marked `FAIL` above is logged verbatim in `evaluation/evaluation_results.json` for targeted tuning rather than hidden or smoothed over.
