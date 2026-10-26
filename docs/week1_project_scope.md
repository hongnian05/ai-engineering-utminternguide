# Semester Project Scoping Document — Week 1

Save as: `docs/week1_project_scope.md`

---

### Project Name
**UTM-InternGuide**: AI-Powered Student Internship Information & Compliance Assistant

---

### Domain
Higher Education / Work-Based Learning & Industrial Training Administration

---

### Problem Statement
Undergraduate students at Universiti Teknologi Malaysia (UTM) face recurring confusion, procedural bottlenecks, and compliance uncertainties when planning and undertaking mandatory industrial training. Key regulations—including credit prerequisites (e.g., minimum 80 accumulated credits), placement qualification criteria, insurance obligations, bi-weekly logbook requirements, and assessment weightages—are dispersed across lengthy PDF handbooks, faculty guidelines, and departmental circulars. Academic advisors and faculty industrial training coordinators are overwhelmed by repetitive administrative inquiries during peak placement periods, leading to delayed advisement and registration errors. An AI-engineered, document-grounded retrieval-augmented system can synthesize accurate, institution-verified answers with direct citations 24/7, reducing coordinator workloads and preventing student compliance failures.

---

### Evidence of the Problem
- **Evidence 1:** Institutional guidelines and prerequisite regulations are fragmented across disparate documents. Students must cross-reference general university policies with faculty-specific manuals and semester circulars to determine eligibility, placement procedures, and grading structures.
  - **Source / citation:** Universiti Teknologi Malaysia, *Buku Peraturan Akademik Program Sarjana Muda Pengajian Sepenuh Masa (Edisi Ke-16)*, Penerbit UTM; and UTM Faculty of Computing, *Industrial Training Guidelines & Student Handbook (2023/2024)*.
- **Evidence 2:** University academic advising and industrial placement coordinators experience significant cognitive overload and communication bottlenecks during pre-placement cycles, with studies showing that more than 60% of coordinator interactions involve repetitive regulatory and eligibility inquiries that divert attention from high-risk student cases.
  - **Source / citation:** Al-Shabandar, R. et al. (2021), "Challenges and AI-Driven Interventions in Higher Education Work-Integrated Learning Administration", *Journal of Educational Technology Systems*; and UTM Academic Management Information System (AMIS) Administrative Reports.

---

### Initial Related Work (at least 3)
- **Study / solution 1:** Human Academic Advising & Faculty Industrial Training Coordinators (UTM Faculty SOPs)
  - **Source / citation:** UTM Faculty of Computing Industrial Training Committee Advisory Workflow (2023).
  - **Key limitation:** Constrained by human working hours, slow turnaround times during peak registration weeks, and vulnerability to inconsistent interpretations of evolving faculty policies across different advisors.
- **Study / solution 2:** Static University FAQ Portals & Downloadable PDF Handbooks (PRISMS / Faculty Web Portal)
  - **Source / citation:** UTM Faculty of Computing Industrial Training Portal (comp.utm.my/industrial-training) and UTM PRISMS (Practical Training Information System).
  - **Key limitation:** Rigid, keyword-reliant search interfaces that fail to resolve complex, multi-conditional student queries (e.g., assessing concurrent credit deficiency with external company placement allowances), requiring tedious manual page-by-page scanning.
- **Study / solution 3:** General-Purpose Commercial AI Chatbots (OpenAI ChatGPT, Anthropic Claude)
  - **Source / citation:** Public Large Language Model services (e.g., GPT-4o, Claude 3.5 Sonnet).
  - **Key limitation:** Lack grounding in proprietary or localized UTM university handbooks and regulations; frequently hallucinate non-existent course codes, credit thresholds, or incorrect assessment rubrics without institutional accountability.

---

### Engineering Gap / Limitation
**What practical or technical limitation remains unresolved?**
- **Gap / Limitation:** Existing approaches force students to choose between slow, resource-constrained human advising or static, fragmented documentation that cannot resolve nuanced, multi-document policy queries. Meanwhile, off-the-shelf general-purpose LLMs lack deterministic grounding in approved UTM institutional handbooks and lack strict guardrails to prevent hallucinated compliance advice that could jeopardize student graduation timelines.

---

### Initial Project Objectives (2–3)
- **O1:** To design an AI-powered, document-grounded question-and-answering system using Retrieval-Augmented Generation (RAG) that ingests, cleans, chunks, and indexes official UTM Industrial Training regulations and handbooks.
- **O2:** To develop the RAG pipeline incorporating dual-layer guardrails (domain-specific input query classification and citation-backed output verification) to eliminate ungrounded or speculative responses.
- **O3:** To evaluate the system objectively across answer groundedness, retrieval accuracy (context precision and recall), response latency (< 3.0 seconds), and safety refusal rates using a curated benchmark of undergraduate internship scenarios.

---

### Target Users
- **Primary Users:** UTM undergraduate students (primarily Year 3 and Year 4 students in Faculty of Computing / Engineering programmes preparing for or completing their industrial training).
- **Secondary Users:** Faculty Industrial Training Coordinators and Academic Advisors who manage student placements and handle compliance escalations.

---

### Data Sources (at least 2)
- **Source 1:** Universiti Teknologi Malaysia Faculty of Computing Undergraduate Industrial Training Handbook & Guidelines (2023/2024) — **URL:** `https://comp.utm.my/wp-content/uploads/2023/10/Handbook-UG-20232024-1.pdf`
- **Source 2:** Buku Peraturan Akademik Program Sarjana Muda Pengajian Sepenuh Masa (UTM Undergraduate Academic Regulations, Edisi Ke-16) — **URL:** `https://academicmanagement.utm.my/wp-content/uploads/2021/08/Buku-Peraturan-Akademik-Sarjana-Muda-Edisi-16.pdf`
- **Source 3:** UTM Centre for Student Development & Industrial Placement Circulars and Guidelines — **URL:** `https://utm.my`

---

### Similar to EduAdvisor
Like the EduAdvisor benchmark, UTM-InternGuide implements a document-grounded RAG architecture utilizing vector embeddings, semantic document retrieval, and prompt guardrails to provide accurate answers directly cited from official institutional PDF documents rather than generating unverified responses.

---

### Different from EduAdvisor
Unlike EduAdvisor (which operates as a general course catalog and prerequisite advisor), UTM-InternGuide addresses the specialized, multi-stage compliance lifecycle of industrial training:
1. **Multi-condition Eligibility Logic:** Resolving complex criteria combining accumulated credit hours, academic standing (Kedudukan Baik / Bersyarat), prerequisite course completions, and semester timing.
2. **Procedural & Deliverable Compliance:** Tracking bi-weekly logbook submission frequencies, employer assessment rubrics, and faculty supervisor site-visit protocols.
3. **Sensitive Exception Handling & Escalation:** Distinguishing informational inquiries from sensitive workplace grievances (e.g., non-payment of allowance, workplace harassment, or safety breaches) and enforcing strict guardrails that immediately route the student to human coordinators and university welfare channels.

---

### Responsible AI Risks (at least 2)
- **Risk 1 — Hallucination of Eligibility / Course Requirements:**
  - *Who is harmed & how:* An ineligible student (e.g., possessing 76 credits instead of the required 80) is mistakenly told by the model that they are eligible. The student signs an internship offer and incurs accommodation expenses, only for the faculty board to reject the registration, delaying graduation by a full academic year.
  - *Engineering Mitigation:* Strict retrieval thresholding, prompt instructions prohibiting ungrounded approvals, and deterministic fallback to the human coordinator when prerequisite context is ambiguous.
- **Risk 2 — Temporal Misalignment / Outdated Policy Ingestion:**
  - *Who is harmed & how:* A student receives outdated grading weightages or expired submission deadlines from an superseded handbook edition, leading to late penalties or failed assessment components.
  - *Engineering Mitigation:* Document metadata tagging (academic session, semester edition), active recency weighting in vector retrieval, and prominent display of policy effective dates with source URLs.
- **Risk 3 — Inappropriate Guidance on High-Stakes Workplace Safety / Grievances:**
  - *Who is harmed & how:* A distressed student facing workplace exploitation, unsafe working conditions, or harassment submits an inquiry, and an automated system provides generic or misleading dispute advice, endangering student well-being.
  - *Engineering Mitigation:* Input guardrails with distress/harassment intent detection that immediately bypass the LLM and output official emergency contact information for the UTM Faculty Industrial Training Coordinator, UTM Counselling Centre, and University Legal Unit.
