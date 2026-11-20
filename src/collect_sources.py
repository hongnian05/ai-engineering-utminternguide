"""
UTM-InternGuide — Official UTM Data Source Collector
Inspects and downloads publicly accessible UTM Industrial Training web pages and PDFs.
Organizes downloads under data/raw/<faculty>/ without modifying existing raw files.
Does NOT bypass paywalls, login restrictions, or download restrictions.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
LOG_PATH = BASE_DIR / "data" / "collection_log.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36 (UTM-InternGuide Academic Research)"
    )
}

WEB_PAGES = [
    {
        "id": "WEB-UGS-001",
        "faculty_dir": "ugs",
        "faculty": "University-Wide (School of Undergraduate Studies)",
        "url": "https://ugs.utm.my/industrial-training-li/",
        "filename": "ugs_industrial_training_li.html",
        "text_filename": "ugs_industrial_training_li.txt",
    },
    {
        "id": "WEB-FKT-001",
        "faculty_dir": "fkt",
        "faculty": "Faculty of Chemical and Energy Engineering",
        "url": "https://fkt.utm.my/li/resources/",
        "filename": "fkt_li_resources.html",
        "text_filename": "fkt_li_resources.txt",
    },
    {
        "id": "WEB-FKE-001",
        "faculty_dir": "fke",
        "faculty": "Faculty of Electrical Engineering",
        "url": "https://fke.utm.my/li/",
        "filename": "fke_li_portal.html",
        "text_filename": "fke_li_portal.txt",
    },
    {
        "id": "WEB-FKM-001",
        "faculty_dir": "fkm",
        "faculty": "Faculty of Mechanical Engineering",
        "url": "https://mech.utm.my/industrial-training-fkm/",
        "filename": "fkm_industrial_training.html",
        "text_filename": "fkm_industrial_training.txt",
    },
]

DIRECT_PDFS = [
    {
        "id": "PDF-UTM-001",
        "faculty_dir": "fkt",
        "faculty": "University-Wide (hosted by FKT)",
        "url": "https://fkt.utm.my/li/wp-content/uploads/sites/216/2022/09/GarisPanduanLI.pdf",
        "filename": "GarisPanduanLI.pdf",
    },
    {
        "id": "PDF-CIVIL-001",
        "faculty_dir": "civil",
        "faculty": "Faculty of Civil Engineering",
        "url": "https://civil.utm.my/spaceska/wp-content/blogs.dir/2494/files/2021/07/Guide-Book-Version-7th-2017-reduced-size.pdf",
        "filename": "Guide-Book-Version-7th-2017-reduced-size.pdf",
    },
    {
        "id": "PDF-MJIIT-001",
        "faculty_dir": "mjiit",
        "faculty": "Malaysia-Japan International Institute of Technology",
        "url": "https://mjiit.utm.my/wp-content/uploads/2015/05/IT-GUIDEBOOK.pdf",
        "filename": "IT-GUIDEBOOK.pdf",
    },
    {
        "id": "PDF-FKM-001",
        "faculty_dir": "fkm",
        "faculty": "Faculty of Mechanical Engineering",
        "url": "https://mech.utm.my/idustrial-training-fkm/wp-content/uploads/sites/245/2026/06/manual_its_pelajar_dis2023-english.pdf",
        "filename": "manual_its_pelajar_dis2023-english.pdf",
    },
]

RESTRICTED_CHECK = [
    {
        "id": "EXT-SCRIBD-001",
        "faculty": "Third-Party / Unverified",
        "url": "https://www.scribd.com/document/981369342/Industrial-Training-Report-Guidelines-UTM",
        "note": "Third-party platform (Scribd); do not bypass paywalls or download restrictions.",
    }
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def extract_clean_html_text(html: str) -> tuple[str, str, list[dict[str, str]]]:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else ""

    # Collect PDF links before stripping navigation
    pdf_links: list[dict[str, str]] = []
    seen_hrefs: set[str] = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if ".pdf" in href.lower() and href not in seen_hrefs:
            seen_hrefs.add(href)
            pdf_links.append({"text": a.get_text(" ", strip=True), "href": href})

    for tag in soup(["script", "style", "noscript", "svg", "iframe"]):
        tag.decompose()

    main = soup.find("main") or soup.find("article") or soup.find(id=re.compile(r"content|main", re.I)) or soup.body
    text = main.get_text("\n", strip=True) if main else soup.get_text("\n", strip=True)
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return title, "\n".join(lines), pdf_links


def fetch_url(url: str, timeout: int = 30) -> requests.Response:
    return requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)


def collect_all() -> dict[str, Any]:
    results: dict[str, Any] = {
        "collected_at_utc": datetime.now(timezone.utc).isoformat(),
        "web_pages": [],
        "direct_pdfs": [],
        "discovered_pdfs": [],
        "restricted_sources": [],
    }

    discovered_candidates: list[dict[str, str]] = []

    # 1. Fetch official UTM web pages
    for item in WEB_PAGES:
        target_dir = RAW_DIR / item["faculty_dir"]
        target_dir.mkdir(parents=True, exist_ok=True)
        entry: dict[str, Any] = dict(item)
        try:
            logger.info("Fetching web page: %s", item["url"])
            resp = fetch_url(item["url"])
            entry["status_code"] = resp.status_code
            entry["final_url"] = resp.url
            entry["content_type"] = resp.headers.get("Content-Type", "")
            if resp.status_code == 200 and "text/html" in entry["content_type"].lower():
                html_path = target_dir / item["filename"]
                text_path = target_dir / item["text_filename"]
                html_path.write_bytes(resp.content)
                title, clean_text, pdf_links = extract_clean_html_text(resp.text)
                text_path.write_text(
                    f"SOURCE URL: {resp.url}\nPAGE TITLE: {title}\n\n{clean_text}\n",
                    encoding="utf-8",
                )
                entry["page_title"] = title
                entry["html_bytes"] = len(resp.content)
                entry["text_chars"] = len(clean_text)
                entry["sha256_text"] = sha256_bytes(text_path.read_bytes())
                entry["saved_text_path"] = str(text_path.relative_to(BASE_DIR))
                entry["pdf_links_found"] = []
                for link in pdf_links:
                    abs_url = urljoin(resp.url, link["href"])
                    entry["pdf_links_found"].append({"text": link["text"], "url": abs_url})
                    if urlparse(abs_url).netloc.endswith("utm.my"):
                        discovered_candidates.append(
                            {
                                "faculty_dir": item["faculty_dir"],
                                "faculty": item["faculty"],
                                "link_text": link["text"],
                                "url": abs_url,
                            }
                        )
                entry["status"] = "downloaded"
                logger.info("Saved %s (%d chars, %d PDF links)", text_path.name, len(clean_text), len(pdf_links))
            else:
                entry["status"] = f"http_{resp.status_code}"
                logger.warning("Non-200 or non-HTML for %s: %s", item["url"], resp.status_code)
        except Exception as exc:
            entry["status"] = "error"
            entry["error"] = str(exc)
            logger.error("Failed fetching %s: %s", item["url"], exc)
        results["web_pages"].append(entry)

    # 2. Fetch direct PDFs
    downloaded_urls: set[str] = set()
    for item in DIRECT_PDFS:
        target_dir = RAW_DIR / item["faculty_dir"]
        target_dir.mkdir(parents=True, exist_ok=True)
        entry = dict(item)
        try:
            logger.info("Downloading PDF: %s", item["url"])
            resp = fetch_url(item["url"], timeout=45)
            entry["status_code"] = resp.status_code
            entry["final_url"] = resp.url
            entry["content_type"] = resp.headers.get("Content-Type", "")
            is_pdf = resp.content[:5] == b"%PDF-" or "pdf" in entry["content_type"].lower()
            if resp.status_code == 200 and is_pdf:
                pdf_path = target_dir / item["filename"]
                pdf_path.write_bytes(resp.content)
                entry["bytes"] = len(resp.content)
                entry["sha256"] = sha256_bytes(resp.content)
                entry["saved_path"] = str(pdf_path.relative_to(BASE_DIR))
                entry["status"] = "downloaded"
                downloaded_urls.add(item["url"].lower())
                downloaded_urls.add(resp.url.lower())
                logger.info("Saved %s (%d bytes)", pdf_path.name, len(resp.content))
            else:
                entry["status"] = f"failed_http_{resp.status_code}"
                logger.warning("PDF download failed for %s: status=%s, content_type=%s", item["url"], resp.status_code, entry["content_type"])
        except Exception as exc:
            entry["status"] = "error"
            entry["error"] = str(exc)
            logger.error("Error downloading %s: %s", item["url"], exc)
        results["direct_pdfs"].append(entry)

    # 3. Download discovered official UTM PDFs linked from UGS/FKT/FKE/FKM pages (limit to relevant guidelines/manuals, max 10)
    seen_disc: set[str] = set(downloaded_urls)
    for cand in discovered_candidates:
        url = cand["url"]
        if url.lower() in seen_disc:
            continue
        seen_disc.add(url.lower())
        filename = Path(urlparse(url).path).name
        if not filename.lower().endswith(".pdf"):
            continue
        # Only download relevant guidelines, manuals, handbooks, calendars, or SOPs
        combined = f"{cand['link_text']} {filename}".lower()
        relevant_kw = ["garis", "panduan", "guide", "manual", "handbook", "its", "li", "training", "internship", "pelajar", "report", "logbook", "syarat", "flow"]
        if not any(k in combined for k in relevant_kw):
            continue
        if len(results["discovered_pdfs"]) >= 10:
            break
        target_dir = RAW_DIR / cand["faculty_dir"]
        target_dir.mkdir(parents=True, exist_ok=True)
        entry = dict(cand)
        entry["filename"] = filename
        try:
            logger.info("Downloading discovered UTM PDF: %s", url)
            resp = fetch_url(url, timeout=45)
            entry["status_code"] = resp.status_code
            entry["final_url"] = resp.url
            if resp.status_code == 200 and resp.content[:5] == b"%PDF-":
                pdf_path = target_dir / filename
                if not pdf_path.exists():
                    pdf_path.write_bytes(resp.content)
                entry["bytes"] = len(resp.content)
                entry["sha256"] = sha256_bytes(resp.content)
                entry["saved_path"] = str(pdf_path.relative_to(BASE_DIR))
                entry["status"] = "downloaded"
                logger.info("Saved discovered PDF: %s (%d bytes)", pdf_path.name, len(resp.content))
            else:
                entry["status"] = f"failed_http_{resp.status_code}"
        except Exception as exc:
            entry["status"] = "error"
            entry["error"] = str(exc)
        results["discovered_pdfs"].append(entry)

    # 4. Respectfully record restricted/third-party sources without bypassing restrictions
    for item in RESTRICTED_CHECK:
        entry = dict(item)
        entry["status"] = "excluded_third_party_restricted"
        entry["downloaded"] = False
        results["restricted_sources"].append(entry)

    LOG_PATH.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info("Collection log saved to %s", LOG_PATH)
    return results


if __name__ == "__main__":
    collect_all()
