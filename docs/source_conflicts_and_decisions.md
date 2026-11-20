# Source Conflicts, Faculty Differences & Engineering Decisions — UTM-InternGuide

* **Application Name:** UTM-InternGuide
* **Author:** Chua Hong Nian (`hongnian05`)
* **Last Updated:** 2026-11-21
* **Principle:** **Never merge or overwrite faculty-specific requirements.** University-wide guidelines provide the institutional baseline; official faculty-specific guidelines take priority for faculty-specific criteria. When evidence is insufficient or outdated, the system explicitly instructs students to confirm with their faculty coordinator.

---

## Summary Matrix of Investigated Conflicts

| Conflict ID | Topic | Conflicting Values Found | Resolution Status | System Rule |
| :---: | :--- | :--- | :---: | :--- |
| **C1** | **Minimum Credit Hours** | 80 credits (FC) vs. 90 credits (FKT, FKE) vs. $\ge 99$ credits (Civil) vs. 70% earned credits (UTM 2024) vs. "determined by faculty" (UTM 2012) | **Resolved (Faculty-Specific, Not Contradictory)** | Filter by student's faculty; ask faculty if unknown. |
| **C2** | **Internship Duration** | 8 weeks vs. 12 weeks (Civil, MJIIT, FKE, FKT) vs. 20 weeks / 1 semester (FC, UTM 2012/2024) | **Resolved (Programme-Specific)** | Never assume 12 or 20 weeks universally; state faculty/programme scope. |
| **C3** | **Digital System Name (PRISMS vs. ITS)** | PRISMS (FC repo excerpt) vs. ITS / `@studentportal` ITS (UTM 2012, UTM 2024, FKM, FKE, FKT, Civil) | **Partially Resolved (Needs FC Verification)** | Prioritize ITS university-wide; note PRISMS only for FC with verification notice. |
| **C4** | **2012 vs. 2024 UTM Senate Guideline** | 2012 Guideline (`GarisPanduanLI.pdf`, hosted 2022) vs. 2024 Senate Guideline (`Final-Garis-Panduan-LI-UTM-2024-Senat.pdf`, approved 30 Apr 2024) | **Resolved (2024 Supersedes 2012)** | Prioritize 2024 Senate Edition; label 2012 edition as historical when retrieved. |
| **C5** | **ITS VPN Access Requirement** | FKT webpage states *"use UTM VPN if not connected with UTM wifi"* vs. Dec 2023/2024 `@studentportal` ITS Manual states *"01. No VPN access"* | **Resolved (Portal Migration)** | Explain new `@studentportal` ITS requires no VPN; legacy `itsv4` URL required VPN. |
| **C6** | **Credit Transfer / Exemption for LI** | 2012 Guideline Sec 10.10 permits credit exemption under strict conditions vs. 2024 Senate Guideline Sec 2.9.11 states *"Pindah Kredit untuk LI adalah tidak dibenarkan"* | **Resolved (2024 Policy Update)** | Cite 2024 Senate Edition as current policy; advise confirming special exemption appeals with UGS/Faculty. |

---

## Detailed Conflict Records

### Conflict C1: Minimum Credit Hour Eligibility (80 vs. 90 vs. 99 vs. 70%)
* **Conflicting Information:**
  1. `FC-REPO-2023-001` (Faculty of Computing, 2023/2024 excerpt): Minimum **80 credit hours** and CGPA $\ge 2.00$ (Kedudukan Baik).
  2. `FKT-WEB-001` (Faculty of Chemical & Energy Engineering, live portal): Completed **3 years of study**, minimum **90 credit gain**, and **CGPA > 2.00**.
  3. `FKE-BRIEF-1-2017` (Faculty of Electrical Engineering, Dec 2017, Page 2): Attained **90 credits** by 2nd semester.
  4. `CIVIL-GUIDE-2017-001` (Faculty of Civil Engineering, 7th Ed. 2017, Page 12): Total Credit (Credit Earned + Credit Transfer + Current Credit) **$\ge 99$**.
  5. `UTM-FKT-2012-001` (UTM Senate 15 Feb 2012, Sec 8.0, Page 4): *"mencapai taraf Kredit Dapat yang ditentukan oleh fakulti"* (credit threshold determined by individual faculties).
  6. `UTM-UGS-2024-001` (UTM Senate 30 Apr 2024, Sec 2.7, Page 6): *"Memperoleh kredit dapat sebanyak 70% daripada jumlah kredit"* (70% of total graduation credits, subject to faculty curriculum).
* **Faculties Involved:** University-Wide, FC, FKT, FKE, Civil Engineering.
* **Relevance & Resolution:** This is **not an error**, but legitimate **faculty-level curriculum variation** (engineering programmes typically require ~130–140 graduation credits, where 70% $\approx$ 91–98 credits; computing programmes typically require ~120–128 credits, where 70% $\approx$ 84–89 credits).
* **Engineering Decision:** Never replace 80 with 90 or merge values. Store strict `faculty` metadata on every chunk. If a user asks *"How many credits do I need?"* without naming their faculty, the chatbot **must ask for their faculty** and note the 2024 university-wide 70% baseline.
* **Further Verification Needed:** Confirm FC's 80-credit rule against the full official 2024/2025 FC Handbook PDF, and verify whether Civil Engineering (2017) and FKE (2017/2018) updated their credit numbers after the April 2024 Senate guideline.

---

### Conflict C2: Internship Duration (8 Weeks vs. 12 Weeks vs. 20 Weeks)
* **Conflicting Information:**
  1. `UTM-UGS-2024-001` (2024 Senate Guideline, Sec 2.6.3, Page 5) and `UTM-FKT-2012-001` (2012 Guideline, Sec 7.1, Page 3): Recognize multiple durations — **8 weeks**, **12 weeks** (short semester), and **1 semester / 20 weeks** depending on programme structure.
  2. `CIVIL-GUIDE-2017-001` (Page 8), `MJIIT-GUIDE-2015-001` (Pages 2–3), `FKE-BRIEF-1-2017` (Page 3), `FKT-WEB-001` (summer break): **12 weeks**.
  3. `FC-REPO-2023-001` (Section 1): **20 weeks** (1 full semester, 12 credit hours).
* **Faculties Involved:** University-Wide, FC, Civil, MJIIT, FKE, FKT.
* **Resolution:** **Resolved.** Engineering faculties generally run 12-week industrial training during the short semester (minimum 8 weeks per EAC standard cited in MJIIT Page 3), whereas Faculty of Computing runs a full 20-week semester internship.
* **Engineering Decision:** Always scope duration answers to the user's faculty; ask for faculty if unspecified.

---

### Conflict C3: Industrial Training System Name (PRISMS vs. ITS)
* **Conflicting Information:**
  1. Existing repo documents (`FC-REPO-2023-001`, `README.md`, `week2_requirements.md`): Refer to **PRISMS** (Practical Training Information System).
  2. Official UTM university-wide and faculty documents (`UTM-UGS-2024-001` Page 7, `UTM-FKT-2012-001` Page 5, `FKM-ITS-2023-001`, `FKE-ITS-MS-2024-001`, `CIVIL-GUIDE-2017-001` Page 10, `FKT-WEB-001`): Officially identify the university system as **ITS (Industrial Training System)**, now integrated into **`@studentportal` ITS**.
* **Faculties Involved:** University-Wide, FKM, FKE, FKT, Civil, FC.
* **Resolution:** **Partially Resolved.** ITS is the verified official UTM-wide system across all newly collected official documents. PRISMS appears only in the local FC excerpt.
* **Engineering Decision:** Refer to **ITS (Industrial Training System / `@studentportal` ITS)** as the official UTM-wide system. Retain PRISMS only when citing the FC excerpt, accompanied by a note advising FC students to confirm whether their current cohort uses `@studentportal` ITS or a faculty-specific portal.
* **Further Verification Needed:** Verify directly with Faculty of Computing Industrial Training Coordinator whether FC currently uses `@studentportal` ITS or PRISMS.

---

### Conflict C4: Superseded 2012 Guideline Hosted Under 2022 FKT URL vs. 2024 Senate Guideline
* **Conflicting Information:**
  * `GarisPanduanLI.pdf` (`https://fkt.utm.my/li/wp-content/uploads/sites/216/2022/09/GarisPanduanLI.pdf`) has a `2022/09` upload URL, but Page 15 proves it was approved by the UTM Senate on **15 February 2012**.
  * `Final-Garis-Panduan-LI-UTM-2024-Senat.pdf` (`ugs.utm.my`) was approved by the UTM Senate on **30 April 2024** (Page 18) and explicitly replaces the 15 February 2012 edition (Page 4).
* **Resolution:** **Resolved.** `UTM-UGS-2024-001` (2024 Senate Edition) is the authoritative university-wide guideline. `UTM-FKT-2012-001` is explicitly tagged `document_version: "2012 Senate Edition (Historical / Superseded)"` so the chatbot never cites it as a 2022 or current guideline.

---

### Conflict C5: VPN Requirement for ITS Access
* **Conflicting Information:**
  * `FKT-WEB-001` (`fkt.utm.my/li/resources/`) links to legacy `http://its.utm.my/itsv4/index.php` and states *"use UTM VPN if not connected with UTM wifi"*.
  * `FKM-ITS-2023-001` (Dec 2023, Page 2) and `FKE-ITS-MS-2024-001` (Mar 2024, Page 2) explicitly highlight **"01. No VPN access"** via the new `@studentportal` ITS using centralized UTMID.
* **Resolution:** **Resolved.** The newer `@studentportal` ITS system eliminates the VPN requirement; the FKT webpage still displays the older `itsv4` link. Both are explained clearly when students ask about ITS login.

---

### Conflict C6: Credit Transfer / Exemption for Industrial Training
* **Conflicting Information:**
  * `UTM-FKT-2012-001` (2012, Sec 10.10, Page 9) outlines conditions for *Pengecualian kredit bagi LI* (credit exemption).
  * `UTM-UGS-2024-001` (2024, Sec 2.9.11, Page 10) states *"Pindah Kredit untuk LI adalah tidak dibenarkan"* (credit transfer for LI is not permitted).
* **Resolution:** **Resolved (2024 takes precedence).** Cite the 2024 Senate policy as authoritative, note the historical 2012 difference if asked, and advise students with prior work experience to confirm any special exemption rules with UGS/Faculty.
