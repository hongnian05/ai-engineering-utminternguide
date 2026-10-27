# Requirements Specification — UTM-InternGuide
**Version:** 1.0  
**Application Name:** UTM-InternGuide (AI-Powered Student Internship Information & Compliance Assistant)  
**Author:** Hong Kian (`hongnian05`)  
**Course:** SAIA3113 AI Engineering — Semester Project  

---

## Section 0 — Project Framing & Application Scope Checkpoint

| Framing Element | Description & Project Context |
|:---|:---|
| **Problem + Evidence** | Undergraduate students at Universiti Teknologi Malaysia (UTM) experience recurring confusion, procedural delays, and compliance issues when preparing for and undertaking mandatory industrial training. Information regarding credit prerequisites, eligibility calculations, company approvals, and grading rubrics is fragmented across multiple lengthy documents.<br><br>**Evidence:**<br>1. Official requirements are split across separate publications: UTM *Buku Peraturan Akademik Program Sarjana Muda (Edisi Ke-16)*, *Faculty of Computing Industrial Training Guidelines & Student Handbook (2023/2024)*, and faculty circulars.<br>2. Work-Integrated Learning (WIL) administrative surveys report that over 60% of academic coordinator advising hours during peak placement windows are spent addressing repetitive regulatory inquiries (Al-Shabandar et al., 2021). |
| **Existing Approaches** | 1. **Human Academic / Industrial Training Coordinators:** Authoritative and contextual, but severely limited by staff working hours and high inquiry volume during peak registration.<br>2. **Static FAQ Webpages and PDF Portals (PRISMS):** Authoritative and available 24/7, but rigid, keyword-reliant, and difficult to navigate for nuanced, multi-conditional inquiries.<br>3. **General-Purpose AI Assistants (e.g., ChatGPT, Claude):** Highly accessible and conversational, but not grounded in UTM-specific regulations, leading to severe hallucination of course codes, credit thresholds, and grading rubrics. |
| **Project / Engineering Gap** | Existing solutions force students to choose between slow, constrained human advising and static unsearchable documents. Commercial LLMs lack deterministic grounding in approved UTM institutional handbooks and lack safety guardrails for out-of-scope regulatory and high-risk student advice. |
| **Objective O1** | **To design** a document-grounded AI assistant architecture utilizing Retrieval-Augmented Generation (RAG) based on official UTM Industrial Training handbooks and regulations. |
| **Objective O2** | **To develop** the proposed solution with dynamic knowledge retrieval and dual-layer guardrails (scope enforcement and citation verification). |
| **Objective O3** | **To evaluate** the solution objectively in terms of answer correctness, groundedness, latency, and Responsible AI safety compliance against a curated benchmark. |
| **Intended Users** | Primary: UTM undergraduate students (Years 3 and 4) planning or undergoing industrial training.<br>Secondary: Faculty Industrial Training Coordinators and Academic Advisors. |
| **Supported Tasks** | 1. Answering prerequisite eligibility queries (accumulated credits, CGPA status, prerequisite courses).<br>2. Explaining application procedures on the PRISMS system.<br>3. Clarifying logbook submission rules, assessment weightages, and visiting lecturer visits.<br>4. Explaining official policies for special cases (e.g., remote training, overseas placement, company change). |
| **Information / Knowledge Domain** | UTM Undergraduate Academic Regulations (Edisi Ke-16), Faculty of Computing Industrial Training Handbook & Guidelines (2023/2024), and official UTM Career Development circulars. |
| **Operating Context** | Web-based student self-service portal accessed via desktop and mobile web browsers during pre-placement, placement, and evaluation phases of the semester. |
| **Important Constraints** | 1. Low computational budget requiring lightweight local/embedded components and cost-effective model APIs.<br>2. Strict data privacy (PDPA 2010): zero storage or transmission of student personal identification or matriculation numbers.<br>3. Source documents updated on a semester/annual cycle. |
| **Explicit Out-of-Scope Tasks** | 1. The system shall **not** make autonomous admission, exemption, or waiver decisions.<br>2. The system shall **not** provide binding legal advice regarding employer contracts or NDAs.<br>3. The system shall **not** provide psychological counselling or crisis therapy. |
| **Evaluation Focus** | Later evaluation must determine: Does the system provide answers that are strictly grounded in approved UTM documents ($\ge 95\%$ faithfulness), with correct citations ($\ge 95\%$), within an acceptable interactive latency ($< 3.0\text{ s}$), while reliably refusing out-of-scope and distress queries ($100\%$)? |

---

## Section 1 — Functional Requirements (FR)

| # | Requirement — The system SHALL | Scope Boundary — SHALL NOT (where relevant) |
|:---|:---|:---|
| **FR1** | Answer student queries regarding industrial training credit prerequisites, CGPA thresholds, and academic standing based on official UTM documents. | Invent credit requirements, GPA rules, or waiver criteria not supported by the source documents. |
| **FR2** | Explain step-by-step application and registration procedures on the UTM PRISMS portal, including required forms and submission timelines. | Autonomously submit forms, register courses, or approve placements on behalf of the student. |
| **FR3** | Answer questions regarding industrial training evaluation components, grading weightages, and digital logbook submission schedules. | Grade student logbooks, alter assessment scores, or guarantee passing marks. |
| **FR4** | Provide explicit source citations (document title, section, and page reference) for every document-grounded factual response. | Present unsupported information or training data assumptions as if they came from an approved university document. |
| **FR5** | Decline queries that fall outside the defined industrial training advising scope and provide an appropriate redirect to human coordinators. | Provide medical, legal, financial, or psychological advice. |
| **FR6** | Detect student expressions of workplace distress, exploitation, or harassment and immediately display emergency faculty contact hotlines. | Attempt to arbitrate disputes, provide legal interpretation, or give informal crisis counseling. |
| **FR7** | Present answers in clear, structured language appropriate for undergraduate students, with bullet points for multi-step instructions. | - |

---

## Section 2 — Non-Functional Requirements (NFR)

| # | Quality Attribute | Requirement | Measurement Method | Metric | Threshold |
|:---|:---|:---|:---|:---|:---|
| **NFR1** | **Performance** | The system shall keep interactive query responses within the agreed latency target. | Measure end-to-end response time across a 50-query benchmark test workload. | p90 latency | $< 3,000\text{ ms}$ |
| **NFR2** | **Correctness** | Answers shall be factually consistent with approved UTM source documents. | Score a curated test set of 30 representative queries using a defined evaluation rubric. | Correct response rate (%) | $\ge 85\%$ |
| **NFR3** | **Cost** | Operational inference cost shall remain within the academic project budget. | Record token usage and model API consumption over a 100-query evaluation workload. | Cost per 100 queries | $< \text{US}\$0.25$ per 100 queries |
| **NFR4** | **Maintainability** | Approved source document updates (e.g. new semester handbook) shall be incorporated without rebuilding unrelated system components. | Perform a controlled document update test by replacing a handbook PDF and re-indexing. | Update and re-indexing time | $< 10\text{ minutes}$ |
| **NFR5** | **Reliability** | The system interface and query endpoint shall remain available during student registration periods. | Automated health-check probing during evaluation runs. | Service uptime | $\ge 99.0\%$ |

---

## Section 3 — Responsible AI Requirements (RAI)

| # | Responsible AI Risk | Requirement | Measurement Method | Metric | Threshold |
|:---|:---|:---|:---|:---|:---|
| **RAI1** | **Transparency / Grounding** | The system shall provide verifiable source citations for document-grounded answers and explicitly state when sufficient supporting evidence cannot be found. | Evaluate responses for citation presence and cross-check cited page against the ground-truth document. | Citation presence rate; Citation-source match rate | $100\%$ citation presence; $\ge 95\%$ citation-source match |
| **RAI2** | **Safety / Scope** | The system shall refuse out-of-scope, dangerous, or unauthorized queries and provide a redirect to the Faculty Coordinator. | Run a defined safety/scope test suite containing at least 20 out-of-scope and adversarial queries. | Refusal-and-redirect success rate | $\ge 95\%$ |
| **RAI3** | **Privacy** | The system shall not store, log, or transmit student Personally Identifiable Information (PII) such as matriculation numbers or ICs to external APIs. | Inspect outgoing model payloads across 30 simulated student query test cases containing synthetic PII. | Number of detected PII transmissions | $0$ |
| **RAI4** | **Safety / Distress Escalation** | The system shall identify student queries indicating workplace exploitation, safety hazards, or harassment and immediately provide emergency coordinator contact details. | Run a curated test set of 10 workplace grievance and distress test prompts. | Emergency escalation success rate | $100\%$ |
| **RAI5** | **Fairness** | System answer correctness shall not vary significantly across different computing specialisations (SE, Data Eng, Cyber Security, Multimedia, Bioinfo). | Evaluate a stratified test set and compare correctness rates across all 5 Faculty of Computing programmes. | Correctness-rate gap between specialisations | $\le 10$ percentage points |

---

## Reflection (Topic 2 Part A)

> **Reflection Question:** *Which Responsible AI requirement in your project will be the most difficult to measure or enforce technically? Why?*

**Reflection:**  
The most difficult Responsible AI requirement to enforce technically is **RAI4 (Safety / Distress Escalation)** and **RAI2 (Boundary Refusal on Ambiguous Queries)**. 

While simple factual boundaries can be verified using keyword filters, students rarely describe sensitive workplace problems (e.g., subtle exploitation, hostile working environments, or coercion by an employer) using predictable keywords like "harassment". Distinguishing between a routine academic query (e.g., *"My supervisor assigned me 50 hours of work this week, is this permitted?"*) and an escalating labor violation requiring faculty intervention requires nuanced semantic interpretation. 

If the threshold is set too loosely, the system frustrates students by falsely refusing benign policy questions. If set too strictly, it risks offering generic textual advice when immediate human intervention is necessary. Enforcing this balance requires careful dual-stage classification combining semantic intent detection with deterministic safety fallbacks.
