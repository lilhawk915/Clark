"""Generate a CSV listing FOIA-required distress sources for Clark County."""

import csv
import json
from pathlib import Path
from typing import Dict, Iterable, List

CONFIG_PATH = Path("configs/clark_county_oh.json")
OUTPUT_CSV = Path("foia/foia_needed.csv")


def load_distress_config(config_path: Path = CONFIG_PATH) -> Dict:
    """Load the Clark County distress configuration JSON."""
    with config_path.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)


def extract_foia_sources(distress_sources: Iterable[Dict]) -> List[Dict]:
    """Return only sources that require FOIA requests."""
    return [source for source in distress_sources if source.get("foia_needed")]


def write_foia_csv(foia_sources: List[Dict], output_path: Path = OUTPUT_CSV) -> None:
    """Write the FOIA source list to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["county", "id", "data_owner", "portal_url", "foia_needed", "notes"]

    with output_path.open("w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for source in foia_sources:
            writer.writerow(
                {
                    "county": "Clark County, OH",
                    "id": source.get("id"),
                    "data_owner": source.get("data_owner"),
                    "portal_url": source.get("portal_url"),
                    "foia_needed": bool(source.get("foia_needed")),
                    "notes": source.get("notes", ""),
                }
            )


def run() -> None:
    """Load distress sources, filter FOIA-needed, and write CSV."""
    config = load_distress_config()
    distress_sources = config.get("distress_sources", [])
    foia_sources = extract_foia_sources(distress_sources)
    write_foia_csv(foia_sources)


if __name__ == "__main__":
    run()
