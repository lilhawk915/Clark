"""Permit report collector for Clark County, Ohio.

This module downloads weekly permit report PDFs using placeholder URLs
and prepares for future parsing. It does not scrape live sites yet.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Iterable, List

import requests

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

CONFIG_PATH = Path("configs/clark_county_oh.json")


def load_config(config_path: Path = CONFIG_PATH) -> Dict:
    """Load the Clark County permit configuration file.

    Args:
        config_path: Path to the JSON configuration.

    Returns:
        Parsed configuration dictionary.
    """
    LOGGER.debug("Loading configuration from %s", config_path)
    with config_path.open("r", encoding="utf-8") as cfg:
        return json.load(cfg)


def ensure_output_directory(output_dir: Path) -> None:
    """Create the output directory if it does not already exist."""
    if not output_dir.exists():
        LOGGER.info("Creating output directory at %s", output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)


def _placeholder_pdf_bytes(source: str) -> bytes:
    """Return placeholder PDF bytes for mocked sources."""
    LOGGER.debug("Generating placeholder PDF content for %s", source)
    return b"%PDF-1.4\n1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n"


def fetch_report(url: str) -> bytes:
    """Fetch a permit report PDF.

    For now, this uses placeholder URLs and avoids scraping live sites.

    Args:
        url: The URL of the permit report.

    Returns:
        Raw PDF bytes.
    """
    if "example.com" in url:
        return _placeholder_pdf_bytes(url)

    # TODO: Replace with real HTTP request once live endpoints are confirmed.
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.content


def download_permit_reports(urls: Iterable[str], output_dir: Path) -> List[Path]:
    """Download permit report PDFs to the output directory."""
    ensure_output_directory(output_dir)
    saved_paths: List[Path] = []

    for url in urls:
        LOGGER.info("Downloading permit report from %s", url)
        pdf_bytes = fetch_report(url)
        filename = url.rstrip("/").split("/")[-1] or "permit_report.pdf"
        if not filename.endswith(".pdf"):
            filename = f"{filename}.pdf"
        pdf_path = output_dir / filename
        LOGGER.debug("Saving permit report to %s", pdf_path)
        with pdf_path.open("wb") as pdf_file:
            pdf_file.write(pdf_bytes)
        saved_paths.append(pdf_path)

    return saved_paths


def parse_permit_report(pdf_path: Path) -> List[Dict[str, str]]:
    """Stub parser for extracting permit details from a report PDF.

    Args:
        pdf_path: Path to the downloaded PDF report.

    Returns:
        A list of permit records with keys: permit_number, address, issue_date,
        permit_type, status.
    """
    LOGGER.info("Parsing permit report at %s", pdf_path)
    # TODO: Implement parsing logic using a PDF parser or OCR as needed.
    return []


def run() -> None:
    """Execute the permit report collection workflow."""
    config = load_config()
    output_dir = Path(config.get("output_directory", "outputs/clark/permits/raw"))
    report_urls = config.get("report_urls", [])

    if not report_urls:
        LOGGER.warning("No report URLs configured; nothing to download.")
        return

    downloaded_reports = download_permit_reports(report_urls, output_dir)

    for report_path in downloaded_reports:
        parse_permit_report(report_path)
        # TODO: Save parsed data to a structured format (e.g., CSV or JSON).


if __name__ == "__main__":
    run()
