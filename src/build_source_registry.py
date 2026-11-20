"""
Generates data/source_registry.json from verified files in data/raw/ with real SHA-256 hashes,
page counts, source classifications (A-F), actual approval/publication dates vs. upload dates,
and access/redistribution notes.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pymupdf

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
REGISTRY_PATH = BASE_DIR / "data" / "source_registry.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def count_pdf_pages(path: Path) -> int | None:
    if path.suffix.lower() != ".pdf":
        return None
    doc = pymupdf.open(path)
    n = len(doc)
    doc.close()
    return n


SOURCES_META: list[dict[str, Any]] = [
    {
        "source_id": "UTM-UGS-2024-001",
        "relative_path": "data/raw/ugs/Final-Garis-Panduan-LI-UTM-2024-Senat.pdf",
        "document_title": "Garis Panduan Latihan Industri Program Sarjana Muda Universiti Teknologi Malaysia (2024)",
        "source_url": "https://ugs.utm.my/wp-content/uploads/sites/8/2024/11/Final-Garis-Panduan-LI-UTM-2024-Senat.pdf",
        "faculty": "University-Wide",
        "department": "Sekolah Pengajian Prasiswazah (UGS), Jabatan TNC (Akademik & Antarabangsa)",
        "publication_or_approval_date": "2024-04-30 (Approved by UTM Senate)",
        "upload_url_date": "2024-11",
        "academic_session": "2024/2025 onwards",
        "document_version": "2024 Senate Edition (Supersedes 2012 Edition)",
        "language": "ms",
        "document_type": "Official University-Wide Guideline",
        "quality_class": "A",
        "main_information": "University-wide industrial training policy: durations (8/12/20 weeks), 70% earned credit rule, ITS usage, prohibition on unapproved company changes, credit transfer rules, evaluation & report timelines.",
        "is_relevant": True,
        "include_in_index": True,
        "access_and_usage_restrictions": "Publicly accessible on official ugs.utm.my portal; UTM institutional copyright — keep raw PDF out of public GitHub redistribution unless authorized.",
    },
    {
        "source_id": "UTM-UGS-2025-002",
        "relative_path": "data/raw/ugs/TERMS-OF-REFERENCE-ToR-–-INTERNATIONAL-INTERNSHIP-PROGRAM-1.pdf",
        "document_title": "Terms of Reference (ToR) — UTM International Internship Program (2025)",
        "source_url": "https://ugs.utm.my/wp-content/uploads/sites/8/2025/04/TERMS-OF-REFERENCE-ToR-%E2%80%93-INTERNATIONAL-INTERNSHIP-PROGRAM-1.pdf",
        "faculty": "University-Wide",
        "department": "School of Undergraduate Studies (UGS)",
        "publication_or_approval_date": "2025",
        "upload_url_date": "2025-04",
        "academic_session": "2025 onwards",
        "document_version": "2025 ToR Edition",
        "language": "en",
        "document_type": "Official University-Wide Guideline",
        "quality_class": "A",
        "main_information": "Governance, eligibility, responsibilities, and procedures for UTM International Internship Program placements.",
        "is_relevant": True,
        "include_in_index": True,
        "access_and_usage_restrictions": "Publicly accessible on ugs.utm.my; institutional copyright applies.",
    },
    {
        "source_id": "UTM-FKT-2012-001",
        "relative_path": "data/raw/fkt/GarisPanduanLI.pdf",
        "document_title": "Garis Panduan Latihan Industri UTM (2012 Senate Edition, hosted by FKT)",
        "source_url": "https://fkt.utm.my/li/wp-content/uploads/sites/216/2022/09/GarisPanduanLI.pdf",
        "faculty": "University-Wide",
        "department": "UTM Senate (hosted by Faculty of Chemical and Energy Engineering)",
        "publication_or_approval_date": "2012-02-15 (Approved by UTM Senate; NOT 2022 despite upload URL)",
        "upload_url_date": "2022-09",
        "academic_session": "2012 onwards (Superseded by 2024 Senate Edition)",
        "document_version": "2012 Senate Edition (Historical / Superseded)",
        "language": "ms",
        "document_type": "Official University-Wide Guideline (Historical)",
        "quality_class": "A",
        "main_information": "Historical UTM-wide guideline: 12-week vs 20-week registration, faculty-determined credit eligibility, ITS system, student insurance (Sec 10.9), credit exemption (Sec 10.10), attendance & fail rules.",
        "is_relevant": True,
        "include_in_index": True,
        "access_and_usage_restrictions": "Publicly accessible on fkt.utm.my; superseded by UTM-UGS-2024-001 — clearly labeled as 2012 edition when cited.",
    },
    {
        "source_id": "FKT-WEB-001",
        "relative_path": "data/raw/fkt/fkt_li_resources.txt",
        "document_title": "FKT Industrial Training Resources & FAQ Webpage",
        "source_url": "https://fkt.utm.my/li/resources/",
        "faculty": "Faculty of Chemical and Energy Engineering",
        "department": "Faculty of Chemical and Energy Engineering (FKT)",
        "publication_or_approval_date": "Live portal (accessed 2026-11-21)",
        "upload_url_date": None,
        "academic_session": "Current",
        "document_version": "Web Snapshot 2026-11-21",
        "language": "en",
        "document_type": "Official Faculty-Specific Guideline (Web)",
        "quality_class": "B",
        "main_information": "FKT eligibility (3 years of study, minimum 90 credits, CGPA > 2.00), summer break timing, ITS-UTM link, VPN requirement, placement sectors.",
        "is_relevant": True,
        "include_in_index": True,
        "access_and_usage_restrictions": "Public official UTM faculty webpage.",
    },
    {
        "source_id": "CIVIL-GUIDE-2017-001",
        "relative_path": "data/raw/civil/Guide-Book-Version-7th-2017-reduced-size.pdf",
        "document_title": "Industrial Training Guidelines for Undergraduate Programme (Faculty of Civil Engineering, 7th Edition)",
        "source_url": "https://civil.utm.my/spaceska/wp-content/blogs.dir/2494/files/2021/07/Guide-Book-Version-7th-2017-reduced-size.pdf",
        "faculty": "Faculty of Civil Engineering",
        "department": "Industrial Training Committee, Faculty of Civil Engineering (FKA/SKA)",
        "publication_or_approval_date": "2017 (7th Edition; uploaded 2021-07)",
        "upload_url_date": "2021-07",
        "academic_session": "2017 onwards",
        "document_version": "7th Edition (2017)",
        "language": "en",
        "document_type": "Official Faculty-Specific Guideline",
        "quality_class": "B",
        "main_information": "Civil Engineering eligibility (>= 99 total credits), >= 12 weeks duration, ITS-UTM workflow, indemnity & insurance letters, logbook, supervisor visits, report writing & assessment rubrics.",
        "is_relevant": True,
        "include_in_index": True,
        "access_and_usage_restrictions": "Publicly accessible on civil.utm.my; institutional copyright applies.",
    },
    {
        "source_id": "MJIIT-GUIDE-2015-001",
        "relative_path": "data/raw/mjiit/IT-GUIDEBOOK.pdf",
        "document_title": "MJIIT Industrial Training Guidebook (As a Reference for Organization, 2015)",
        "source_url": "https://mjiit.utm.my/wp-content/uploads/2015/05/IT-GUIDEBOOK.pdf",
        "faculty": "Malaysia-Japan International Institute of Technology",
        "department": "Malaysia-Japan International Institute of Technology (MJIIT), UTM Kuala Lumpur",
        "publication_or_approval_date": "2015",
        "upload_url_date": "2015-05",
        "academic_session": "2015 onwards",
        "document_version": "2015 Edition",
        "language": "en",
        "document_type": "Official Faculty-Specific Guideline",
        "quality_class": "B",
        "main_information": "MJIIT compulsory 12-week internship (Malaysia or Japan), EAC minimum 8-week standard, insurance (Malaysia & Mitsui Sumitomo Japan), English report submission within 2 weeks, evaluation marks distribution.",
        "is_relevant": True,
        "include_in_index": True,
        "access_and_usage_restrictions": "Publicly accessible on mjiit.utm.my; verify with MJIIT coordinator whether a newer post-2015 edition exists.",
    },
    {
        "source_id": "FKM-ITS-2023-001",
        "relative_path": "data/raw/fkm/manual_its_pelajar_dis2023-english.pdf",
        "document_title": "Portal Usage Guideline for Industrial Training @studentportal ITS (English, Dec 2023)",
        "source_url": "https://mech.utm.my/idustrial-training-fkm/wp-content/uploads/sites/245/2026/06/manual_its_pelajar_dis2023-english.pdf",
        "faculty": "Faculty of Mechanical Engineering",
        "department": "Faculty of Mechanical Engineering (FKM) / UTM ITS",
        "publication_or_approval_date": "2023-12 (December 2023; hosted under 2026/06 URL)",
        "upload_url_date": "2026-06",
        "academic_session": "2023/2024 onwards",
        "document_version": "December 2023 English Manual",
        "language": "en",
        "document_type": "Official ITS System Manual",
        "quality_class": "C",
        "main_information": "Step-by-step student portal ITS usage: No VPN needed via studentportal, UTMID login, company placement application, offer acceptance, insurance document download, online placement appeal.",
        "is_relevant": True,
        "include_in_index": True,
        "access_and_usage_restrictions": "Publicly accessible on mech.utm.my; applies broadly to UTM ITS users as well as FKM.",
    },
    {
        "source_id": "FKM-WEB-001",
        "relative_path": "data/raw/fkm/fkm_industrial_training.txt",
        "document_title": "FKM Industrial Training Portal Webpage",
        "source_url": "https://mech.utm.my/industrial-training-fkm/",
        "faculty": "Faculty of Mechanical Engineering",
        "department": "Faculty of Mechanical Engineering (FKM)",
        "publication_or_approval_date": "Live portal (Sem 3 2025/2026 notices)",
        "upload_url_date": None,
        "academic_session": "2025/2026",
        "document_version": "Web Snapshot 2026-11-21",
        "language": "en",
        "document_type": "Official Faculty-Specific Guideline (Web)",
        "quality_class": "B",
        "main_information": "Links to FKM forms (BLP-01 confirmation, BLP-02 supervisor evaluation, company guidebook, ITS manual).",
        "is_relevant": True,
        "include_in_index": True,
        "access_and_usage_restrictions": "Public official UTM faculty webpage.",
    },
    {
        "source_id": "FKE-WEB-001",
        "relative_path": "data/raw/fke/fke_li_portal.txt",
        "document_title": "FKE Industrial Training (Latihan Industri) Portal Webpage",
        "source_url": "https://fke.utm.my/li/",
        "faculty": "Faculty of Electrical Engineering",
        "department": "Faculty of Electrical Engineering (FKE)",
        "publication_or_approval_date": "Live portal (accessed 2026-11-21)",
        "upload_url_date": None,
        "academic_session": "Current",
        "document_version": "Web Snapshot 2026-11-21",
        "language": "en",
        "document_type": "Official Faculty-Specific Guideline (Web)",
        "quality_class": "B",
        "main_information": "FKE industrial training overview, committee organization, announcements, procedures, ITS manuals, and downloadable forms.",
        "is_relevant": True,
        "include_in_index": True,
        "access_and_usage_restrictions": "Public official UTM faculty webpage.",
    },
    {
        "source_id": "FKE-ITS-EN-2024-001",
        "relative_path": "data/raw/fke/Student-Manual-english.pdf",
        "document_title": "Portal Usage Guideline for Industrial Training @studentportal ITS (FKE English Manual)",
        "source_url": "https://fke.utm.my/wp-content/uploads/2024/03/Student-Manual-english.pdf",
        "faculty": "Faculty of Electrical Engineering",
        "department": "Faculty of Electrical Engineering (FKE) / UTM ITS",
        "publication_or_approval_date": "2024-03 (upload date; same @studentportal ITS system)",
        "upload_url_date": "2024-03",
        "academic_session": "2023/2024 onwards",
        "document_version": "2024 English Manual",
        "language": "en",
        "document_type": "Official ITS System Manual",
        "quality_class": "C",
        "main_information": "English ITS @studentportal usage manual (duplicate/variant of FKM ITS English manual; excluded from duplicate embedding if identical).",
        "is_relevant": True,
        "include_in_index": False,
        "access_and_usage_restrictions": "Publicly accessible on fke.utm.my; deduplicated against FKM-ITS-2023-001 to prevent duplicate retrieval noise.",
    },
    {
        "source_id": "FKE-ITS-MS-2024-001",
        "relative_path": "data/raw/fke/Manual-Pelajar-malay.pdf",
        "document_title": "Panduan Pengguna Bagi Latihan Industri @studentportal ITS (Bahasa Melayu)",
        "source_url": "https://fke.utm.my/wp-content/uploads/2024/03/Manual-Pelajar-malay.pdf",
        "faculty": "University-Wide",
        "department": "UTM ITS (hosted by FKE)",
        "publication_or_approval_date": "2024-03",
        "upload_url_date": "2024-03",
        "academic_session": "2023/2024 onwards",
        "document_version": "2024 Bahasa Melayu Manual",
        "language": "ms",
        "document_type": "Official ITS System Manual",
        "quality_class": "C",
        "main_information": "Bahasa Melayu guide to using @studentportal ITS: UTMID login without VPN, placement application, email notifications, online placement appeal.",
        "is_relevant": True,
        "include_in_index": True,
        "access_and_usage_restrictions": "Publicly accessible on fke.utm.my.",
    },
    {
        "source_id": "FKE-BRIEF-1-2017",
        "relative_path": "data/raw/fke/Taklimat-LI-Part-I-5-Dec-2017.pdf",
        "document_title": "FKE LI Briefing Part I (SKE* 4926 — Semester III 2017/2018)",
        "source_url": "https://fke.utm.my/wp-content/uploads/2023/02/Taklimat-LI-Part-I-5-Dec-2017.pdf",
        "faculty": "Faculty of Electrical Engineering",
        "department": "Industrial Training Working Committee, FKE",
        "publication_or_approval_date": "2017-12-05 (uploaded 2023-02)",
        "upload_url_date": "2023-02",
        "academic_session": "2017/2018 (Historical briefing)",
        "document_version": "Part I Briefing (Dec 2017)",
        "language": "en",
        "document_type": "Supporting Document (Faculty Briefing)",
        "quality_class": "E",
        "main_information": "FKE compulsory subject (6 credits), 90 credits attained by 2nd semester, 12 weeks duration, ITS registration & application statuses (Pending/Approved/Accepted/Rejected after 3 weeks).",
        "is_relevant": True,
        "include_in_index": True,
        "access_and_usage_restrictions": "Publicly accessible on fke.utm.my; historical briefing (2017/2018) — verify current session dates with FKE.",
    },
    {
        "source_id": "FKE-BRIEF-2-2018",
        "relative_path": "data/raw/fke/Taklimat-LI-Part-II-22-May-2018.pdf",
        "document_title": "FKE LI Briefing Part II (SKE* 4926 — Semester III 2017/2018)",
        "source_url": "https://fke.utm.my/wp-content/uploads/2023/02/Taklimat-LI-Part-II-22-May-2018.pdf",
        "faculty": "Faculty of Electrical Engineering",
        "department": "Industrial Training Working Committee, FKE",
        "publication_or_approval_date": "2018-05-22 (uploaded 2023-02)",
        "upload_url_date": "2023-02",
        "academic_session": "2017/2018 (Historical briefing)",
        "document_version": "Part II Briefing (May 2018)",
        "language": "en",
        "document_type": "Supporting Document (Faculty Briefing)",
        "quality_class": "E",
        "main_information": "FKE online logbook submission in ITS, signed page upload, faculty supervisor assignment, online evaluation, company change rules.",
        "is_relevant": True,
        "include_in_index": True,
        "access_and_usage_restrictions": "Publicly accessible on fke.utm.my; historical briefing (2017/2018).",
    },
    {
        "source_id": "FKE-FORM-001",
        "relative_path": "data/raw/fke/1.-Application-of-Potential-Company-for-Industrial-Training.pdf",
        "document_title": "Permohonan Cadangan Syarikat Baru Latihan Industri (Application of Potential Company Form)",
        "source_url": "https://fke.utm.my/wp-content/uploads/2023/04/1.-Application-of-Potential-Company-for-Industrial-Training.pdf",
        "faculty": "Faculty of Electrical Engineering",
        "department": "Sekretariat Unit Pembangunan dan Kerjaya / FKE",
        "publication_or_approval_date": "Undated (uploaded 2023-04)",
        "upload_url_date": "2023-04",
        "academic_session": None,
        "document_version": "Official Form",
        "language": "ms/en",
        "document_type": "Official Application Form",
        "quality_class": "D",
        "main_information": "Form for proposing a new host company not yet listed in the ITS database.",
        "is_relevant": True,
        "include_in_index": True,
        "access_and_usage_restrictions": "Publicly accessible official form.",
    },
    {
        "source_id": "FC-REPO-2023-001",
        "relative_path": "data/raw/utm_fc_industrial_training_handbook_2023_2024.txt",
        "document_title": "UTM Faculty of Computing Undergraduate Industrial Training Handbook & Guidelines (Repo Excerpt, 2023/2024)",
        "source_url": "https://comp.utm.my/wp-content/uploads/2023/10/Handbook-UG-20232024-1.pdf",
        "faculty": "Faculty of Computing",
        "department": "Faculty of Computing (FC)",
        "publication_or_approval_date": "2023/2024 (Repository structured excerpt)",
        "upload_url_date": "2023-10",
        "academic_session": "2023/2024",
        "document_version": "2023/2024 (Local Excerpt — Pending Full Official FC PDF Verification)",
        "language": "en",
        "document_type": "Official Faculty-Specific Guideline (Local Excerpt)",
        "quality_class": "B",
        "main_information": "FC 20-week internship (12 credits), 80 credit hours minimum, CGPA >= 2.00 (KB), PRISMS workflow, 40/30/30 assessment weightage, bi-weekly logbook, Act 174 & workplace grievance escalation.",
        "is_relevant": True,
        "include_in_index": True,
        "access_and_usage_restrictions": "Existing local repository text excerpt; verify against full official comp.utm.my PDF.",
    },
    {
        "source_id": "UTM-REG-ED16-001",
        "relative_path": "data/raw/utm_academic_regulations_edisi_16.txt",
        "document_title": "Buku Peraturan Akademik Program Sarjana Muda Pengajian Sepenuh Masa (Edisi Ke-16, Repo Excerpt)",
        "source_url": "https://academicmanagement.utm.my/wp-content/uploads/2021/08/Buku-Peraturan-Akademik-Sarjana-Muda-Edisi-16.pdf",
        "faculty": "University-Wide",
        "department": "Jabatan Pengurusan Akademik, UTM",
        "publication_or_approval_date": "2021/2022 (Edisi Ke-16; Local Excerpt)",
        "upload_url_date": "2021-08",
        "academic_session": "2021/2022 onwards",
        "document_version": "Edisi Ke-16 (Local Excerpt)",
        "language": "ms",
        "document_type": "Official University-Wide Academic Regulation (Local Excerpt)",
        "quality_class": "A",
        "main_information": "Academic standing definitions (KB >= 2.00, KS 1.70-1.99, KG < 1.70), semester credit loads, HL/HG Pass/Fail grading, 90% attendance, deferment & appeal procedures.",
        "is_relevant": True,
        "include_in_index": True,
        "access_and_usage_restrictions": "Existing local repository text excerpt; verify against full official Edisi Ke-16 PDF.",
    },
    {
        "source_id": "EXT-SCRIBD-001",
        "relative_path": None,
        "document_title": "Industrial Training Report Guidelines UTM (Scribd Upload)",
        "source_url": "https://www.scribd.com/document/981369342/Industrial-Training-Report-Guidelines-UTM",
        "faculty": "Unverified / Third-Party",
        "department": "Unverified Third-Party Uploader (Scribd)",
        "publication_or_approval_date": "Unknown",
        "upload_url_date": None,
        "academic_session": None,
        "document_version": "Unverified",
        "language": "en",
        "document_type": "Third-Party / Unverified Document",
        "quality_class": "F",
        "main_information": "Third-party hosted UTM Industrial Training Report Guidelines.",
        "is_relevant": False,
        "include_in_index": False,
        "access_and_usage_restrictions": "EXCLUDED: Third-party platform with paywall/download restrictions; unverified official status. Not downloaded or indexed.",
    },
]


def build_registry() -> dict[str, Any]:
    entries = []
    for meta in SOURCES_META:
        item = dict(meta)
        rel = item.get("relative_path")
        if rel:
            full_path = BASE_DIR / rel
            if full_path.exists():
                item["file_exists"] = True
                item["file_size_bytes"] = full_path.stat().st_size
                item["sha256"] = sha256_file(full_path)
                item["num_pages"] = count_pdf_pages(full_path)
            else:
                item["file_exists"] = False
                item["file_size_bytes"] = 0
                item["sha256"] = None
                item["num_pages"] = None
        else:
            item["file_exists"] = False
            item["file_size_bytes"] = 0
            item["sha256"] = None
            item["num_pages"] = None
        entries.append(item)

    registry = {
        "registry_version": "2.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "total_sources": len(entries),
        "indexed_sources": sum(1 for e in entries if e["include_in_index"] and e["file_exists"]),
        "excluded_sources": sum(1 for e in entries if not e["include_in_index"]),
        "sources": entries,
    }
    REGISTRY_PATH.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {REGISTRY_PATH} ({registry['total_sources']} total, {registry['indexed_sources']} indexed).")
    return registry


if __name__ == "__main__":
    build_registry()
