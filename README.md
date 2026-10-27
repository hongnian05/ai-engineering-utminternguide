# UTM-InternGuide — AI-Powered Student Internship Information & Compliance Assistant

> Delivers instant, document-grounded guidance to UTM undergraduate students regarding industrial training eligibility, application procedures, logbook compliance, and regulations, strictly grounded in official university handbooks.

---

## Problem Statement
Undergraduate students at Universiti Teknologi Malaysia (UTM) frequently face procedural delays, conflicting information, and compliance confusion when preparing for and undertaking mandatory industrial training. Key regulations regarding prerequisite credits, placement approvals, logbook submission schedules, and grading rubrics are dispersed across lengthy PDF guidelines and departmental circulars, overwhelming academic coordinators with repetitive queries during peak registration cycles. UTM-InternGuide provides an AI-engineered, document-grounded 24/7 assistant that provides accurate, policy-verified answers with exact citations, streamlining the advising process and preventing registration failures.

---

## Evidence of the Problem
- **Fragmented Institutional Documentation:** Prerequisite criteria and placement regulations are dispersed across disparate official publications, including the university-wide *Buku Peraturan Akademik Sarjana Muda (Edisi Ke-16)* and faculty-level *Faculty of Computing Industrial Training Guidelines*, requiring students to cross-examine multi-source documents manually.
  *(Source: UTM Academic Management & Faculty of Computing Publications, 2023)*
- **Administrative Coordinator Overload:** Academic advisors and internship committee staff spend over 60% of advising time answering routine eligibility and submission inquiries, leading to delayed communication and peak-season bottlenecks.
  *(Source: Al-Shabandar et al., 2021, "Challenges and AI-Driven Interventions in Higher Education Work-Integrated Learning Administration")*

---

## Initial Related Work / Existing Approaches
- **Human Academic & Faculty Industrial Training Coordinators:** Authoritative and highly contextual, but constrained by limited office hours, heavy advising loads during placement deadlines, and potential variance in verbal interpretations across staff.
  *(Source: UTM Faculty Industrial Training Committee Advising Workflow; Key limitation: High latency and non-scalable availability)*
- **Static University FAQ Webpages & Downloadable PDF Portals:** Authoritative and publicly accessible via the faculty web portal and PRISMS system, but rigid and unable to resolve complex multi-variable conditions (e.g., credit deficiencies combined with overseas placement exemptions).
  *(Source: UTM PRISMS / Faculty of Computing Industrial Training Portal; Key limitation: Static keyword search and manual navigation burden)*
- **General-Purpose Commercial AI Models (ChatGPT, Claude):** Conversational and accessible 24/7, but entirely ungrounded in UTM-specific institutional rules, resulting in hallucinations of incorrect credit thresholds, non-existent course codes, and unverified academic requirements.
  *(Source: Public OpenAI / Anthropic Foundation Models; Key limitation: High hallucination rate and lack of institutional grounding)*

---

## Engineering Gap / Limitation
Current solutions either rely on labor-intensive human advising that cannot scale during peak placement periods or depend on static document downloads that fail to answer nuanced, multi-document student queries. In contrast, ungrounded commercial LLMs present severe hallucination risks when applied to university compliance. An engineering gap remains for a localized, document-grounded RAG system equipped with dual-layer safety guardrails and deterministic citation mechanisms tailored to UTM industrial training regulations.

---

## Project Objectives
- **O1:** To design an AI-powered, document-grounded question-and-answering system using Retrieval-Augmented Generation (RAG) that ingests, cleans, chunks, and semantically indexes official UTM Industrial Training regulations and handbooks.
- **O2:** To develop the RAG pipeline incorporating dual-layer guardrails (domain-specific input query classification and citation-backed output verification) to eliminate ungrounded or speculative responses.
- **O3:** To evaluate the system objectively across answer groundedness, retrieval accuracy (context precision and recall), response latency (< 3.0 seconds), and safety refusal rates using a curated benchmark of undergraduate internship scenarios.

---

## Target Users
- **Primary Users:** UTM undergraduate students (primarily Year 3 and Year 4 students in computing and engineering disciplines planning or completing industrial training).
- **Secondary Users:** Faculty Industrial Training Coordinators and Academic Advisors who manage student placements and monitor compliance.

---

## Data Sources
- **Source 1:** Universiti Teknologi Malaysia Faculty of Computing Undergraduate Industrial Training Handbook & Guidelines (2023/2024) — [comp.utm.my Handbook](https://comp.utm.my/wp-content/uploads/2023/10/Handbook-UG-20232024-1.pdf)
- **Source 2:** Buku Peraturan Akademik Program Sarjana Muda Pengajian Sepenuh Masa (UTM Undergraduate Academic Regulations, Edisi Ke-16) — [academicmanagement.utm.my](https://academicmanagement.utm.my/wp-content/uploads/2021/08/Buku-Peraturan-Akademik-Sarjana-Muda-Edisi-16.pdf)
- **Source 3:** UTM Career Centre & Industrial Placement Policy Circulars — [utm.my](https://utm.my)

---

## Repository Structure
```
ai-engineering-utminternguide/
├── README.md                          # Project overview and weekly engineering log
├── docs/                              # Engineering documentation and lab deliverables
│   ├── week1_observation_sheet.md     # Topic 1 Part A: AI system observation report
│   ├── week1_system_map.png           # Topic 1 Part B: Conceptual AI system map diagram
│   ├── week1_project_scope.md         # Topic 1 Part C: Detailed project scoping document
│   ├── week2_requirements.md          # Topic 2 Part A: Project framing, scope, FRs, NFRs & RAI
│   ├── week2_evaluation_criteria.md   # Topic 2 Part B: Evaluation criteria table & benchmark design
│   ├── week2_architecture_v1.png      # Topic 2 Part C: V1 system architecture diagram (300 DPI)
│   └── week2_architecture_decisions.md# Topic 2 Part C: ADRs, trade-offs & Traceability Matrix (RTM)
├── data/                              # Raw and processed official policy documents (untracked/gitkeep)
│   └── .gitkeep
├── src/                               # Application source code (RAG pipeline, retrieval, guardrails)
│   └── .gitkeep
├── notebooks/                         # Experimental prototyping & data exploration notebooks
│   └── .gitkeep
├── evaluation/                        # Evaluation benchmarks, test datasets, and metric scripts
│   └── .gitkeep
└── prompts/                           # System prompts, guardrail prompts, and prompt templates
    └── .gitkeep
```

---

## Weekly Progress
| Week | Focus | Deliverable | Status |
|:---:|:---|:---|:---:|
| **W1** | System map + project scope | README + docs | ✅ |
| **W2** | Requirements, Architecture & Evaluation Criteria | Requirements, Evaluation Benchmarks, V1 Architecture & ADRs | ✅ |
| **W3** | Data Ingestion & Document Chunking | Data Pipeline Scripts | ⏳ Pending |
| **W4** | Vector Embeddings & Retrieval | Vector Store Setup | ⏳ Pending |
| **W5** | Prompt Engineering & RAG Generation | Pipeline Integration | ⏳ Pending |
| **W6** | Guardrails & Safety Controls | Safety Layer Evaluation | ⏳ Pending |
| **W7** | System Evaluation & Performance Benchmarking | Evaluation Report | ⏳ Pending |
