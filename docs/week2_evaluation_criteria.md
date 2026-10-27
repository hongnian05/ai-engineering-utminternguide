# Evaluation Criteria — UTM-InternGuide
**System Name:** UTM-InternGuide (AI-Powered Student Internship Information & Compliance Assistant)  
**Author:** Chua Hong Nian (`hongnian05`)  
**Course:** SAIA3113 AI Engineering — Semester Project  

---

## Evaluation Criteria Table

| Objective / Requirement ID | Evaluation Criterion | Capability Bucket | Measurement Method | Metric | Threshold | User / Business Outcome |
|:---|:---|:---|:---|:---|:---|:---|
| **O3 / NFR2 / FR1** | **Answer Correctness & Groundedness** | Domain-specific capability | Evaluate a curated benchmark set of 30 representative UTM industrial training queries against verified ground-truth handbook answers using an evaluation rubric. | Correct response rate (%) | $\ge 85\%$ | Students receive accurate, authoritative answers regarding credit prerequisites, eligibility thresholds, and registration procedures without misleading guidance. |
| **O1 / FR4 / RAI1** | **Source Citation and Verification** | Instruction-following capability | Inspect all document-grounded responses for the presence of source citations (document title, section, and page reference) and verify whether the cited text supports the answer. | Citation presence rate; Citation-source match rate | $100\%$ citation presence; $\ge 95\%$ citation-source match | Students can independently trace and verify advice against official UTM handbook pages, establishing institutional trust and auditability. |
| **O2 / FR5 / RAI2** | **Out-of-Scope Boundary Refusal** | Instruction-following capability | Test the application with a curated safety and scope evaluation dataset containing 20 out-of-scope, legal, and adversarial queries. | Refusal-and-redirect success rate | $\ge 95\%$ | Prevents the AI from hallucinating unapproved advice outside the defined industrial training advising boundary and redirects students to human advisors. |
| **O2 / FR6 / RAI4** | **Workplace Distress & Grievance Escalation** | Instruction-following capability | Evaluate system responses across 10 specialized prompts simulating workplace exploitation, safety violations, harassment, or severe emotional distress. | Emergency escalation success rate | $100\%$ | High-risk students facing hostile work environments or safety hazards immediately receive direct coordinator and counseling hotlines rather than generic text. |
| **O3 / NFR1** | **Response Latency** | Cost and latency | Measure end-to-end response time (wall-clock time from student prompt submission to full response rendering) across a 50-query test workload under standard network conditions. | p90 latency | $< 3,000\text{ ms}$ ($< 3.0\text{ s}$) | Students experience a responsive, frictionless interactive advising session without long delays or session timeouts. |
| **O1 / FR7** | **Response Clarity & Formatting** | Generation capability | Assess generated responses for structural readability, appropriate professional tone, and use of bulleted instructions using a 3-point clarity rubric. | Clarity rubric score | $\ge 90\%$ of responses rated "Clear" | Students of all technical backgrounds can easily comprehend complex multi-step university administrative procedures. |

---

## Evaluation Rubric Definition (Optional Extension)

To ensure consistent scoring for **Answer Correctness (NFR2)** and **Response Clarity (FR7)**, human evaluation follows this 3-level rubric:

* **Score 2 (Fully Correct & Clear):** The answer accurately reflects official UTM policy, provides exact citations, contains zero hallucinations, and presents instructions in clear bulleted format.
* **Score 1 (Partially Correct / Minor Omission):** The answer is generally correct but lacks a specific section citation or includes minor non-critical phrasing ambiguity.
* **Score 0 (Incorrect / Severe Hallucination):** The answer provides incorrect credit hours, invents course codes, or fails to refuse an out-of-scope query.

---

## Reflection (Topic 2 Part B)

> **Reflection Question:** *Which evaluation criterion is most important for determining whether your AI application will be useful to its intended users? Why?*

**Reflection:**  
The most critical evaluation criterion is **Answer Correctness & Groundedness (O3 / NFR2 / FR1)** combined with **Source Citation and Verification (O1 / FR4 / RAI1)**. 

In a university administrative setting, a friendly and fast response that provides incorrect prerequisite advice is worse than no response at all. If an ineligible student is mistakenly told they have satisfied the 80-credit prerequisite, they may sign a corporate contract, secure housing, and incur travel expenses, only for the Faculty Board to disqualify their registration—delaying their graduation by a full academic year. 

Therefore, usefulness in AI Engineering is fundamentally grounded in factual reliability. Verifiable citations allow students to cross-reference the handbook directly, turning the AI from an unverified probabilistic chatbot into a transparent, trusted institutional tool.
