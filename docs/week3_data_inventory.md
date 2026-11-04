# Data Inventory & Inspection Checkpoint — Week 3

**Save as:** `docs/week3_data_inventory.md`  
**Application Name:** UTM-InternGuide (AI-Powered Student Internship Information & Compliance Assistant)  
**Author:** Chua Hong Nian (`hongnian05`)  
**Course:** SAIA3113 AI Engineering — Semester Project  
**Repository:** [ai-engineering-utminternguide](https://github.com/hongnian05/ai-engineering-utminternguide)  

---

## 1. Project Data Inventory Table

| Source ID | Filename / URL | Type & Purpose | Version / Date / Owner | Access / Rights | Inspection Evidence |
|:---:|:---|:---|:---|:---|:---|
| **S01** | `utm_fc_industrial_training_handbook_2023_2024.pdf`<br>(and `.txt` text extract)<br>[comp.utm.my Handbook URL](https://comp.utm.my/wp-content/uploads/2023/10/Handbook-UG-20232024-1.pdf) | **Unstructured Text & Structured Policy Tables:** Defines internship prerequisites (80 credit hours, CGPA $\ge 2.00$, Kedudukan Baik), PRISMS registration procedures, assessment weightages (40% Industry, 30% Visiting Lecturer, 30% Faculty Committee), and logbook submission rules. | Academic Session 2023/2024 (Pindaan Oktober 2023).<br>**Owner:** Faculty of Computing, Universiti Teknologi Malaysia. | **Public / Authorised:** Publicly accessible academic guidelines published on the official UTM Faculty of Computing portal for student advising. | **Inspection Evidence:**<br>• Extracted characters: 5,612<br>• Sections identified: 6 comprehensive policy sections<br>• Table layout: Preserves 3-way assessment breakdown and PRISMS 5-step workflow<br>• SHA-256 fingerprint: Verified in `week3_manifest.json` |
| **S02** | `utm_academic_regulations_edisi_16.pdf`<br>(and `.txt` text extract)<br>[academicmanagement.utm.my URL](https://academicmanagement.utm.my/wp-content/uploads/2021/08/Buku-Peraturan-Akademik-Sarjana-Muda-Edisi-16.pdf) | **Unstructured Regulatory Text:** Cross-institutional graduation statutes governing undergraduate academic standing (KB vs. KS), minimum semester credit loads, and Pass/Fail (HL/HG) grading rules for industrial training. | Edisi Ke-16 (Pindaan 2021/2022).<br>**Owner:** Jabatan Pengurusan Akademik, UTM. | **Public / Authorised:** Official university academic regulation publication released for full-time undergraduate students. | **Inspection Evidence:**<br>• Extracted characters: 3,418<br>• Sections identified: 5 parts (Bahagian 1–5)<br>• Regulatory grounding: Establishes statutory definition of Kedudukan Baik and credit standing<br>• SHA-256 fingerprint: Verified in `week3_manifest.json` |

---

## 2. Checkpoint A: Topic 2 Requirements Traceability to Data Needs

| Requirement ID | Needed Information / Feature | Candidate Source | Why Usable & Relevant Quality / Safety Concern |
|:---|:---|:---|:---|
| **FR1 / NFR2** (Prerequisite Eligibility & Correctness) | Accumulated credit threshold ($\ge 80$ credits), CGPA threshold ($\ge 2.00$), and required core subjects. | **S01** (Section 2) & **S02** (Bahagian 2 & 3) | **Usability:** Authoritative institutional rules.<br>**Quality / Safety:** Hallucinating credit requirements could cause an ineligible student to accept an internship and face disqualification. Grounding strictly in S01/S02 eliminates hallucination. |
| **FR2** (PRISMS Workflow) | Procedural sequence for application, offer letter upload, coordinator endorsement, and indemnity forms. | **S01** (Section 3) | **Usability:** Contains exact 5-step application roadmap.<br>**Quality Concern:** Missing sequential steps causes registration bottlenecks. |
| **FR3** (Assessment & Logbook Schedule) | Bi-weekly submission frequency, late penalties (10%/week), and grading component breakdown (40% / 30% / 30%). | **S01** (Sections 4 & 5) | **Usability:** Deterministic numerical breakdown.<br>**Quality Concern:** Naive chunking could slice the assessment percentage table. |
| **FR4 / RAI1** (Source Citation & Grounding) | Explicit document title, academic session, section, and page provenance. | **S01 & S02** metadata headers | **Usability:** Enables verifiable citations appended to student responses.<br>**Quality / Safety:** Guarantees 100% citation presence and traceable provenance. |
| **FR6 / RAI4** (Workplace Distress Escalation) | Contact coordinates for Faculty Coordinator and Student Counselling Centre for workplace grievances. | **S01** (Section 6) | **Safety Concern:** Student distress must trigger deterministic emergency hotlines rather than speculative LLM advice. |

---

## 3. Representative Loaded Inspection Samples

### Sample 1: S01 — UTM Faculty of Computing IT Handbook (Section 2: Prerequisites)
```text
SECTION 2: STUDENT ELIGIBILITY CRITERIA AND PREREQUISITES
To qualify for registration and placement in the Industrial Training programme, an undergraduate candidate must strictly fulfill the following prerequisite conditions prior to the commencement semester:
1. Accumulated Credit Threshold: The student must have completed and accumulated a minimum of eighty (80) credit hours of academic courses within their respective programme curriculum.
2. Academic Standing: The student must hold an active academic status of Good Standing (Kedudukan Baik, KB) with a Cumulative Grade Point Average (CGPA) of at least 2.00 at the time of application and registration. Students under Conditional Standing (Kedudukan Bersyarat, KS) are strictly prohibited from undergoing industrial training until their academic standing is restored to KB.
3. Compulsory Core Subjects: The student must have completed and passed all Year 1 and Year 2 core computing faculty subjects, including Data Structures and Algorithms, Object-Oriented Programming, Database Systems, and System Analysis and Design.
```
*Observable Properties:* Clean alphanumeric text; numbered list hierarchy; explicit numerical thresholds (80 credits, 2.00 CGPA); zero missing fields.

### Sample 2: S01 — Assessment Scheme (Section 4: Evaluation Breakdown)
```text
SECTION 4: EVALUATION SCHEME AND ASSESSMENT WEIGHTAGE
The Industrial Training course is evaluated continuously throughout the 20-week placement:
1. Industrial Supervisor Assessment (Host Company): 40% Weightage (assessing technical competence, punctuality, and workplace contribution).
2. Faculty Visiting Lecturer Assessment (Academic Supervisor): 30% Weightage (assessing student presentation, project demo, and supervisor interview).
3. Faculty Industrial Training Committee Assessment: 30% Weightage (bi-weekly digital logbook 10%, comprehensive final technical report 20%).
Grading Standard: To obtain a Pass (Lulus) grade, a student must secure an overall aggregated mark of at least sixty percent (60%) and achieve at least 50% in each individual assessment component.
```
*Observable Properties:* Clear multi-variable numerical distribution; percentages sum exactly to 100%; explicit Pass/Fail criteria (60% overall, 50% per component).

---

## 4. Storage Architecture & Provenance Governance

```
data/
├── raw/                              # Read-only original source documents (immutable baseline)
│   ├── utm_fc_industrial_training_handbook_2023_2024.pdf
│   ├── utm_fc_industrial_training_handbook_2023_2024.txt
│   ├── utm_academic_regulations_edisi_16.pdf
│   └── utm_academic_regulations_edisi_16.txt
│
├── processed/                        # Reusable Part B prepared outputs (prepared_text.jsonl)
│   └── prepared_text.jsonl
│
├── pipeline_v1/                      # Executable Part C pipeline output with stage manifests
│   └── documents/
│       ├── prepared_text.jsonl
│       └── pipeline_manifest.json
│
└── week3_manifest.json               # Part B cryptographic SHA-256 lineage registry
```

* **Data Safety & PDPA Compliance:** All documents in `data/raw/` contain public university policies and regulatory statutes. No student names, matriculation numbers, or confidential industrial agreements are stored or processed.
* **Lineage Tracking:** Every prepared chunk is cryptographically linked back to its raw source file via SHA-256 hashes recorded in `week3_manifest.json`.
