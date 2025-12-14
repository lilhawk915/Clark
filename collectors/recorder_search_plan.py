"""Generate Recorder search plan CSV from Clark County configuration."""

import csv
import json
from pathlib import Path
from typing import Dict, Iterable, List, Tuple, Union

CONFIG_PATH = Path("configs/clark_county_oh.json")
OUTPUT_PATH = Path("outputs/clark/recorder/search_plan.csv")


def load_distress_config(config_path: Path = CONFIG_PATH) -> Dict:
    """Load the Clark County distress configuration JSON."""
    with config_path.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)


def select_sources_with_search_strategy(distress_sources: Iterable[Dict]) -> List[Dict]:
    """Return sources that define a search strategy."""
    return [source for source in distress_sources if source.get("search_strategy")]


def format_date_range(date_range: Union[Dict, str, int, None]) -> str:
    """Convert date range structure into a string value."""
    if isinstance(date_range, dict):
        range_type = date_range.get("type")
        range_value = date_range.get("value")
        if range_type and range_value is not None:
            return f"{range_type}:{range_value}"
        return "" if range_type is None and range_value is None else str(date_range)
    if date_range is None:
        return ""
    return str(date_range)


def normalize_document_entry(entry: Union[str, Dict]) -> Tuple[str, str]:
    """Extract document type and optional notes from a document type entry."""
    if isinstance(entry, dict):
        document_type = entry.get("type") or entry.get("name") or ""
        notes = entry.get("notes", "")
        return document_type, notes
    return str(entry), ""


def write_search_plan(sources: List[Dict], output_path: Path = OUTPUT_PATH) -> None:
    """Write the recorder search plan CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["source_id", "portal_url", "document_type", "date_range", "notes"]

    with output_path.open("w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for source in sources:
            search_strategy = source.get("search_strategy", {})
            document_types = search_strategy.get("document_types", [])
            date_range_value = format_date_range(search_strategy.get("date_range"))
            strategy_notes = search_strategy.get("notes", "")

            for document_entry in document_types:
                document_type, document_notes = normalize_document_entry(document_entry)
                writer.writerow(
                    {
                        "source_id": source.get("id"),
                        "portal_url": source.get("portal_url"),
                        "document_type": document_type,
                        "date_range": date_range_value,
                        "notes": document_notes or strategy_notes,
                    }
                )


def run() -> None:
    """Generate the recorder search plan CSV."""
    config = load_distress_config()
    distress_sources = config.get("distress_sources", [])
    recorder_sources = select_sources_with_search_strategy(distress_sources)
    write_search_plan(recorder_sources)


if __name__ == "__main__":
    run()
