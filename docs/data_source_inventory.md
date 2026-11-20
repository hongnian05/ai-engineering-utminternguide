# Official Data Source Inventory — UTM-InternGuide

* **Application Name:** UTM-InternGuide
* **Author:** Chua Hong Nian (`hongnian05`)
* **Structured Registry:** [`data/source_registry.json`](../data/source_registry.json)
* **Last Verified:** 2026-11-21

---

## 1. Source Quality Classification Framework

| Class | Category | Indexing Priority |
| :---: | :--- | :--- |
| **A** | Official university-wide guidelines (UTM Senate / UGS / Academic Management) | Highest (General Policy Baseline) |
| **B** | Official faculty-specific guidelines & official faculty web portals | Highest (Overrides general baseline for faculty-specific criteria) |
| **C** | Official Industrial Training System (ITS) user manuals | High (Procedural / System Usage) |
| **D** | Official application forms & templates | Medium (Supporting procedural forms) |
| **E** | Supporting documents (official faculty briefing slides, procedures) | Medium (Clearly labeled with historical session dates) |
| **F** | Third-party or unverified documents (e.g., Scribd) | **Excluded** (Never indexed without official verification) |

---

## 2. Complete Source Inventory Table

| Source ID | Class | Document Title | Faculty / Scope | Actual Publication / Approval Date | Upload URL Date | Session / Version | Lang | Pages | Indexed? | Access & Redistribution Note |
| :--- | :---: | :--- | :--- | :--- | :---: | :--- | :---: | :---: | :---: | :--- |
| `UTM-UGS-2024-001` | **A** | Garis Panduan Latihan Industri Program Sarjana Muda UTM (2024) | University-Wide (UGS) | **2024-04-30** (UTM Senate) | 2024-11 | 2024 Senate Edition (Supersedes 2012) | `ms` | 20 | Yes | Public on `ugs.utm.my`; institutional copyright — do not redistribute raw PDF publicly without permission. |
| `UTM-UGS-2025-002` | **A** | Terms of Reference (ToR) — UTM International Internship Program | University-Wide (UGS) | **2025** | 2025-04 | 2025 ToR Edition | `en` | 17 | Yes | Public on `ugs.utm.my`; institutional copyright. |
| `UTM-FKT-2012-001` | **A** | Garis Panduan Latihan Industri UTM (hosted by FKT) | University-Wide (Historical) | **2012-02-15** (UTM Senate — **NOT 2022**) | 2022-09 | 2012 Senate Edition (Superseded by 2024) | `ms` | 16 | Yes (Tagged Historical) | Public on `fkt.utm.my`; retained for historical reference & conflict resolution, clearly tagged as 2012. |
| `UTM-REG-ED16-001` | **A** | Buku Peraturan Akademik Sarjana Muda (Edisi Ke-16, Local Excerpt) | University-Wide | **2021/2022** (Excerpt) | 2021-08 | Edisi Ke-16 (Repo Excerpt) | `ms` | N/A (TXT) | Yes | Existing repo excerpt; full official PDF should be verified against `academicmanagement.utm.my`. |
| `FC-REPO-2023-001` | **B** | UTM Faculty of Computing IT Handbook & Guidelines (Local Excerpt) | Faculty of Computing | **2023/2024** (Excerpt) | 2023-10 | 2023/2024 (Repo Excerpt) | `en` | N/A (TXT) | Yes | Existing repo excerpt; pending verification against full official FC PDF. |
| `FKT-WEB-001` | **B** | FKT Industrial Training Resources & FAQ Webpage | Faculty of Chemical & Energy Engineering | Live portal (2026-11-21) | N/A | Web Snapshot | `en` | N/A (Web) | Yes | Public official `fkt.utm.my/li/resources/`. |
| `CIVIL-GUIDE-2017-001` | **B** | Industrial Training Guidelines for Undergraduate Programme (7th Ed.) | Faculty of Civil Engineering | **2017** (7th Edition) | 2021-07 | 7th Edition (2017) | `en` | 37 | Yes | Public on `civil.utm.my`; institutional copyright. |
| `MJIIT-GUIDE-2015-001` | **B** | MJIIT Industrial Training Guidebook (Reference for Organization) | MJIIT (UTM KL) | **2015** | 2015-05 | 2015 Edition | `en` | 6 | Yes | Public on `mjiit.utm.my`; confirm with MJIIT if a post-2015 edition exists. |
| `FKE-WEB-001` | **B** | FKE Industrial Training Portal Webpage | Faculty of Electrical Engineering | Live portal (2026-11-21) | N/A | Web Snapshot | `en` | N/A (Web) | Yes | Public official `fke.utm.my/li/`. |
| `FKM-WEB-001` | **B** | FKM Industrial Training Portal Webpage | Faculty of Mechanical Engineering | Live portal (Sem 3 2025/2026) | N/A | Web Snapshot | `en` | N/A (Web) | Yes | Public official `mech.utm.my/industrial-training-fkm/`. |
| `FKM-ITS-2023-001` | **C** | Portal Usage Guideline for Industrial Training @studentportal ITS (EN) | Faculty of Mechanical Engineering / UTM ITS | **2023-12** (Dec 2023) | 2026-06 | Dec 2023 English Manual | `en` | 21 | Yes | Public on `mech.utm.my`; note upload URL is 2026/06 while document is Dec 2023. |
| `FKE-ITS-MS-2024-001` | **C** | Panduan Pengguna Bagi Latihan Industri @studentportal ITS (BM) | University-Wide (hosted by FKE) | **2024-03** | 2024-03 | 2024 BM Manual | `ms` | 21 | Yes | Public on `fke.utm.my`; Bahasa Melayu counterpart of ITS manual. |
| `FKE-ITS-EN-2024-001` | **C** | Portal Usage Guideline @studentportal ITS (FKE EN copy) | Faculty of Electrical Engineering | **2024-03** | 2024-03 | 2024 EN Manual | `en` | 21 | **No (Dedup)** | Duplicate/near-duplicate of `FKM-ITS-2023-001`; stored in `data/raw/fke/` but excluded from index to avoid duplicate retrieval. |
| `FKE-FORM-001` | **D** | Permohonan Cadangan Syarikat Baru Latihan Industri | Faculty of Electrical Engineering | Undated | 2023-04 | Official Form | `ms/en` | 3 | Yes | Public official form on `fke.utm.my`. |
| `FKE-BRIEF-1-2017` | **E** | FKE LI Briefing Part I (SKE* 4926 — Sem III 2017/2018) | Faculty of Electrical Engineering | **2017-12-05** | 2023-02 | Historical Briefing (2017/2018) | `en` | 12 | Yes (Tagged Historical) | Public on `fke.utm.my`; explicitly tagged as 2017/2018 historical briefing. |
| `FKE-BRIEF-2-2018` | **E** | FKE LI Briefing Part II (SKE* 4926 — Sem III 2017/2018) | Faculty of Electrical Engineering | **2018-05-22** | 2023-02 | Historical Briefing (2017/2018) | `en` | 15 | Yes (Tagged Historical) | Public on `fke.utm.my`; explicitly tagged as 2017/2018 historical briefing. |
| `EXT-SCRIBD-001` | **F** | Industrial Training Report Guidelines UTM (Scribd) | Unverified / Third-Party | Unknown | N/A | Unverified | `en` | Unknown | **No (Excluded)** | **Excluded:** Third-party platform with paywall/download restrictions; unverified provenance. Not downloaded. |

---

## 3. Key Date Discrepancies Verified During Collection

1. **`GarisPanduanLI.pdf` (FKT URL `2022/09` vs. Approval `15 February 2012`):** Page 15 explicitly states *"Disahkan oleh Senat Universiti Teknologi Malaysia pada 15 Februari 2012"*. It was merely uploaded to FKT's WordPress site in September 2022.
2. **`Final-Garis-Panduan-LI-UTM-2024-Senat.pdf` (UGS URL `2024/11` vs. Approval `30 April 2024`):** Page 18 explicitly records Senate approval on `30/4/2024`, and Page 4 states it replaces the 15 February 2012 guideline.
3. **`Guide-Book-Version-7th-2017-reduced-size.pdf` (Civil URL `2021/07` vs. Edition `2017`):** Page 2 states *Seventh Edition 2017*, uploaded to WordPress in July 2021.
4. **`manual_its_pelajar_dis2023-english.pdf` (FKM URL `2026/06` vs. Content `Disember 2023`):** Filename and content are the December 2023 manual, re-hosted under a `2026/06` URL path.

---

## 4. Copyright & Repository Redistribution Policy

* **Official UTM PDFs** are publicly accessible for student use on `*.utm.my`, but remain copyright of Universiti Teknologi Malaysia.
* In `.gitignore`, downloaded official PDFs under `data/raw/*/*.pdf` should be excluded from public GitHub commits unless written institutional redistribution permission is obtained, while `data/source_registry.json`, `docs/data_source_inventory.md`, and `src/collect_sources.py` allow any authorized user to reproduce the exact local raw corpus with SHA-256 verification.
